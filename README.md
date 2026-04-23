# Protus - Programmable Recon & Offensive Toolkit for Unified Systems

```
░█████████                         ░██                          
░██     ░██                        ░██                          
░██     ░██ ░██░████  ░███████  ░████████ ░██    ░██  ░███████  
░█████████  ░███     ░██    ░██    ░██    ░██    ░██ ░██        
░██         ░██      ░██    ░██    ░██    ░██    ░██  ░███████  
░██         ░██      ░██    ░██    ░██    ░██   ░███        ░██ 
░██         ░██       ░███████      ░████  ░█████░██  ░███████  

Developed by RetroGuy1336
```

## Overview

**Protus** is a programmable reconnaissance and offensive toolkit designed to assist cybersecurity professionals and penetration testers in their security assessments. It provides a unified framework for network reconnaissance, vulnerability analysis, and payload delivery through an interactive command-line interface.

The framework is built with modularity and extensibility in mind, allowing security researchers to perform systematic network exploration and testing against target systems.

## Features

### 🔍 Reconnaissance Modules

#### **Port Scanner**
- Full TCP port scanning using Scapy for raw packet manipulation
- SYN scan technique for stealth and efficiency
- Service identification (FTP, SSH, TELNET, SMTP, DNS, HTTP, HTTPS, MySQL, RDP, Redis, MongoDB, etc.)
- Customizable port ranges (first port to last port)
- Adjustable stealth modes (0-4) to control scanning speed and detectability
  - Mode 0: Aggressive (no delay)
  - Mode 1-3: Balanced
  - Mode 4: Stealthy (1.5s delay between packets)

#### **DNS Lookup**
- Domain name resolution
- Multi-address retrieval (IPv4 and IPv6 support)
- Duplicate IP filtering
- Network reconnaissance and information gathering

### 💣 Payload Engine

The integrated payload management system provides:

- **Multiple Payload Categories:**
  - **SQLi**: SQL Injection payloads
  - **XSS**: Cross-Site Scripting payloads
  - **LFI**: Local File Inclusion payloads
  - **SSTI**: Server-Side Template Injection payloads

- **Wordlist Integration:**
  - Local payload storage in `/payloads/` directory
  - SecLists integration support for enhanced wordlists
  - Lazy-loading for memory efficiency with large datasets

- **Mutation Engine:**
  - URL encoding (single and double)
  - Case variation mutations
  - Null byte injection
  - Comment injection techniques
  - Unicode encoding
  - Configurable mutation depth for WAF bypass strategies

- **Context-Aware Generation:**
  - OS-specific payloads (Linux/Windows for LFI)
  - Context-sensitive XSS wrappers (HTML attributes, etc.)
  - On-demand payload streaming

### 🔎 Exploit Database Search

#### **ExploitDB Integration**
- Direct search integration with Exploit-DB (https://www.exploit-db.com)
- Real-time vulnerability and exploit lookup
- Automated web browser integration for instant access to exploit details
- Support for vulnerability queries with parameter-based search
- Streamlined command-line interface for quick exploit research

**Usage:**
```
pts >> start exploitdb
PTS_ExploitDB >> exploitdb --search <vulnerability_name>
```

Example:
```
PTS_ExploitDB >> exploitdb --search "Apache RCE"
```

This will automatically open your default web browser with the Exploit-DB search results for the specified vulnerability.

## Architecture

```
Protus/
├── protus.py              # Main entry point with interactive menu
├── banners.py             # Random ASCII banner generator
├── requirements.txt       # Python dependencies
├── core/
│   ├── config.py          # Command parser and configuration
│   └── payloads.py        # Payload engine and mutation logic
├── modules/
│   ├── exploitdb/
│   │   ├── exploitdb.py   # Exploit-DB search module
│   │   └── parser.py      # Argument parsing for exploitdb tool
│   └── recon/
│       ├── dnslookup.py   # DNS resolution module
│       ├── portscanner.py # TCP port scanning module
│       └── parser.py      # Argument parsing for recon tools
└── payloads/
    ├── sqli.txt           # SQL Injection wordlist
    ├── xss.txt            # XSS payload wordlist
    └── lfi.txt            # Local File Inclusion wordlist
```

## Installation

### Prerequisites
- The OS must be Linux-based (Ubuntu, Kali, etc.) for optimal compatibility with Scapy and raw socket operations
- Python 3.10+
- pip (Python package manager)
- Root/Administrator privileges (required for raw packet operations with Scapy)
- Internet connection (for downloading dependencies and potential future updates)

### Setup

1. **Clone or download the repository:**
   ```bash
   cd /path/to/Protus
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```


## Usage

### Starting Protus

Run the main application:
```bash
sudo python3 protus.py
```

You will see an interactive menu:
```
pts >> 
```

### Available Commands

#### View Framework Information
```bash
pts >> show
pts >> show --more
```

Displays version information and framework description.

#### List Available Resources
```bash
pts >> list payloads     # Display available payload types
```

#### Access Reconnaissance Tools

```bash
pts >> start recon
```

This opens the reconnaissance submenu where you can choose between:

##### **Port Scanner (Option 0)**

Command format:
```
scan <host> -Fp <first_port> -Lp <last_port> -St <stealth_mode>
```

Example:
```
PTS_Scanner >> scan 192.168.1.1 -Fp 20 -Lp 1000 -St 2
```

This will:
- Scan ports 20-1000 on host 192.168.1.1
- Use stealth mode 2 (0.3 second delay between packets)
- Display open ports with associated service names
- Filter results by status (Open, Filtered, etc.)

##### **DNS Lookup (Option 1)**

Command format:
```
lookup -u <target_url>
```

Example:
```
PTS_Lookup >> lookup -u example.com
```

This will:
- Resolve the domain name
- Display all discovered IP addresses
- Remove duplicate addresses
- Handle resolution errors gracefully

#### Access Exploit Database Search

```bash
pts >> start exploitdb
```

This opens the Exploit-DB search submenu where you can search for vulnerabilities and exploits.

##### **ExploitDB Search**

Command format:
```
exploitdb --search <vulnerability_or_exploit_name>
```

Example:
```
PTS_ExploitDB >> exploitdb --search RCE Apache Struts
```

This will:
- Search the Exploit-DB database for matching vulnerabilities
- Open your default web browser with detailed exploit information
- Display the search URL in the console
- Allow you to browse exploit details, POC code, and metadata

## How It Works

### Reconnaissance Workflow

1. **User starts Protus** → Interactive menu loads
2. **User selects a module** → Recon tools become available
3. **User chooses a tool** (Port Scanner or DNS Lookup)
4. **Arguments are parsed** → Command-line arguments validated
5. **Scan/Lookup executes** → Scapy sends packets or DNS queries
6. **Results are displayed** → Open services and IPs shown with color formatting

### Payload Workflow

1. **Load wordlist** → Internal or SecLists sources
2. **Stream payloads** → Lazy-load for memory efficiency
3. **Apply mutations** → Generate WAF-bypass variations
4. **Context filtering** → Apply OS or platform-specific logic
5. **Deliver payloads** → Integrate with scanning results

## Dependencies

- **Scapy 2.7.0** - Network packet manipulation library for raw socket operations

## Color Coding

Protus uses ANSI color codes for enhanced readability:
- **Red** (`\033[1;31m`) - Titles and banners
- **Blue** (`\033[1;34m`) - User input prompts
- **Default** (`\033[m`) - Standard output

## Security Considerations

⚠️ **Legal Notice**: Protus is designed for authorized security testing and educational purposes only. Unauthorized access to computer systems is illegal.

- Always obtain proper authorization before conducting security assessments
- Use Protus only in controlled environments or with explicit written permission
- Understand the legal implications of port scanning and security testing in your jurisdiction
- Ensure your network traffic complies with organizational policies

## Future Enhancements

- Additional reconnaissance modules (WHOIS lookup, traceroute, etc.)
- Automated vulnerability detection
- Export results in multiple formats (JSON, CSV, HTML)
- Advanced filtering for ExploitDB search results
- Multi-threading for faster scans
- GUI interface option
- Proxy support for anonymized scanning
- Local exploit database caching for offline searches

## Contributing

This project is actively maintained by RetroGuy1336. For contributions, suggestions, or bug reports, please review the project structure and test your changes thoroughly.

## License

This project is provided as-is for educational and authorized security testing purposes.

---

**Version:** 0.1.2v  
**Developer:** RetroGuy1336  
**Last Updated:** 2026
