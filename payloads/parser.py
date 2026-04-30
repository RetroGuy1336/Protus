import argparse
import shlex
import os
from pathlib import Path
import importlib

red    = '\033[1;31m'
blue   = '\033[1;34m'
green  = '\033[1;32m'
yellow = '\033[1;33m'
limit  = '\033[m'


def discover_exploits() -> dict:
    exploits = {}
    exploits_dir = Path("payloads/exploits")

    # FIX 1: usa enumerate só nos arquivos válidos (sem __init__.py)
    # filtra primeiro, depois enumera — garante IDs 0, 1, 2...
    valid_files = [
        f for f in sorted(exploits_dir.rglob("*.py"))
        if not f.name.startswith("__")
    ]

    for i, file in enumerate(valid_files):
        module_name = f"payloads.exploits.{file.stem}"

        try:
            mod = importlib.import_module(module_name)

            # FIX 2: busca a classe pelo atributo NAME dentro do módulo,
            # em vez de adivinhar o nome pelo stem do arquivo
            cls = None
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                if (
                    isinstance(attr, type)
                    and hasattr(attr, "NAME")
                    and hasattr(attr, "run")
                    and hasattr(attr, "info")
                ):
                    cls = attr
                    break

            exploits[str(i)] = {
                "name":        file.stem,
                "module":      module_name,
                "class":       cls.__name__ if cls else None,
                "description": getattr(cls, "DESCRIPTION", "No description") if cls else "N/A",
                "cve":         getattr(cls, "CVE", "N/A") if cls else "N/A",
            }

        except Exception as e:
            print(f"[!] Skipping {file.name}: {e}")

    return exploits


AVAILABLE_EXPLOITS = discover_exploits()


def list_exploits():
    if not AVAILABLE_EXPLOITS:
        print(yellow + "\n  [!] Nenhum exploit encontrado em payloads/exploits/" + limit)
        return
    print(yellow + "\n  Available Exploits:" + limit)
    print("  " + "-=" * 30)
    for key, exploit in AVAILABLE_EXPLOITS.items():
        cve = f"[{exploit['cve']}]" if exploit['cve'] != "N/A" else ""
        print(f"  [{key}]  {exploit['name']:<20} {cve:<20} {exploit['description']}")
    print("  " + "-=" * 30)


def load_exploit(exploit_info: dict):
    """Importa e retorna uma instância do exploit."""
    try:
        mod = importlib.import_module(exploit_info["module"])
        if exploit_info["class"]:
            cls = getattr(mod, exploit_info["class"])
            return cls()
        return mod
    except ImportError as e:
        print(red + f"[-] Falha ao carregar '{exploit_info['module']}': {e}" + limit)
        return None


def exploit_parser(user_input: str, exploit_obj):
    """Faz o parse de run/info e despacha para o exploit."""
    parser = argparse.ArgumentParser(prog="Protus Exploit")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_p = subparsers.add_parser("run")
    run_p.add_argument("-t", "--target",  required=True, help="Host/IP alvo")
    run_p.add_argument("-p", "--port",    type=int, default=80, help="Porta alvo (padrão: 80)")
    run_p.add_argument("--timeout",       type=int, default=5,  help="Timeout em segundos")
    run_p.add_argument("--verbose",       action="store_true")

    subparsers.add_parser("info")

    try:
        args = parser.parse_args(shlex.split(user_input))
    except SystemExit:
        return

    if args.command == "info":
        exploit_obj.info()
    elif args.command == "run":
        exploit_obj.run(args)


def attack_parser():
    os.system("clear")
    print(green + "\n  Starting Protus Exploit Engine..." + limit)
    print(f"""
  {red}Use Exploit - Protus Framework{limit}
  {'-=' * 30}
  Comandos:
    list              - Lista os exploits disponíveis
    use <id>          - Seleciona um exploit pelo ID
    info              - Mostra detalhes do exploit selecionado
    run -t <host>     - Executa o exploit selecionado
    help              - Mostra esta mensagem
    back              - Volta ao menu principal
  {'-=' * 30}""")

    selected_exploit = None
    exploit_obj      = None

    while True:
        label = f"({selected_exploit['name']})" if selected_exploit else ""
        try:
            user = input(blue + f"pts_exploit{label} >> " + limit).strip()
        except (KeyboardInterrupt, EOFError):
            print()
            break

        if not user:
            continue

        tokens = user.split()
        cmd    = tokens[0].lower()

        if cmd == "list":
            list_exploits()

        elif cmd == "use":
            if len(tokens) < 2:
                print(red + "[-] Uso: use <id>  (rode 'list' para ver os IDs)" + limit)
                continue
            eid = tokens[1]
            if eid not in AVAILABLE_EXPLOITS:
                print(red + f"[-] ID '{eid}' não encontrado. Rode 'list' primeiro." + limit)
                continue
            selected_exploit = AVAILABLE_EXPLOITS[eid]
            exploit_obj      = load_exploit(selected_exploit)
            if exploit_obj is None:
                selected_exploit = None
                continue
            print(green + f"[+] Selecionado: {selected_exploit['name']}" + limit)
            print(f"    {selected_exploit['description']}")
            print("    Digite 'info' para detalhes ou 'run -t <host>' para executar.")

        elif cmd in ("run", "info"):
            if not selected_exploit or not exploit_obj:
                print(red + "[-] Nenhum exploit selecionado. Use 'use <id>' primeiro." + limit)
                continue
            exploit_parser(user, exploit_obj)

        elif cmd == "options":
            if not selected_exploit:
                print(red + "[-] Nenhum exploit selecionado." + limit)
                continue
            print(yellow + f"\n  Opções de {selected_exploit['name']}:" + limit)
            print(f"  {'Nome':<12} {'Valor':<20} {'Obrigatório':<12} Descrição")
            print("  " + "-" * 60)
            for nome, opt in exploit_obj.OPTIONS.items():
                valor    = opt["value"] or "não definido"
                required = "sim" if opt["required"] else "não"
                print(f"  {nome:<12} {valor:<20} {required:<12} {opt['description']}")

        elif cmd == "set":
            if len(tokens) < 3:
                print(red + "[-] Uso: set <OPÇÃO> <valor>" + limit)
                continue
            opt_name = tokens[1].upper()
            opt_val  = tokens[2]
            if opt_name not in exploit_obj.OPTIONS:
                print(red + f"[-] Opção '{opt_name}' não existe. Use 'options' para ver as disponíveis." + limit)
                continue
            exploit_obj.OPTIONS[opt_name]["value"] = opt_val
            print(green + f"[+] {opt_name} => {opt_val}" + limit)

        elif cmd == "unset":
            if len(tokens) < 2:
                print(red + "[-] Uso: unset <OPÇÃO>" + limit)
                continue
            opt_name = tokens[1].upper()
            if opt_name in exploit_obj.OPTIONS:
                exploit_obj.OPTIONS[opt_name]["value"] = None
                print(green + f"[+] {opt_name} limpo." + limit)

        elif cmd == "help":
            print("""
  list              - Lista os exploits disponíveis
  use <id>          - Seleciona exploit pelo ID
  info              - Detalhes do exploit atual
  run -t <host> [-p <porta>] [--timeout <s>] [--verbose]
  back              - Volta ao menu principal
""")

        elif cmd == "back":
            break

        else:
            print(red + f"[-] Comando '{cmd}' desconhecido. Digite 'help'." + limit)