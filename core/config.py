import argparse
from modules.recon.parser import ParserRecon
from modules.exploitdb.parser import ExploitDB_Parser
from payloads.parser import attack_parser
import pathlib

red = '\033[1;31m'
limit = '\033[m'

def arguments(command):
    parser = argparse.ArgumentParser(prog="Protus", description="Protus parser")

    subparsers = parser.add_subparsers(dest='comando')
    show_parser = subparsers.add_parser('show', help="It shows some things of Protus")
    show_parser.add_argument('--more', action="store_true")
    show_parser.add_argument("commands")

    list_parser = subparsers.add_parser("list")
    list_sub = list_parser.add_subparsers(dest="type")

    list_sub.add_parser("payloads")
    list_sub.add_parser("modules")
    list_sub.add_parser("--more")

#-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    start_parser = subparsers.add_parser('start', help="It starts a module from Protus")
    start_sub = start_parser.add_subparsers(dest="modulo")
    recon_parser = start_sub.add_parser("recon")
    db_parser = start_sub.add_parser("exploitdb")

    use_parser = subparsers.add_parser("use", help="Use payloads, exploits, enconders and more")
    use_sub = use_parser.add_subparsers(dest="attack")
    exploits_parser = use_sub.add_parser("exploit")

    try:
        args = parser.parse_args(command.split())
    except SystemExit:
        print("Command not found...")
        return
        
    if args.comando == 'show':
        print("""
Protus, The Framework for Pentest
Version: 0.1.2v
Description: Protus, The Framework for Pentest is a tool to assist offensive cybersecurity engineers in their work""")
        if args.more:
            print("No")
        elif args.commands:
            print("-=" * 58)
            print("Current commands: show, show --more, show commands"
                  "list payloads, list modules"
                  "start recon, start exploitdb")

    if args.comando == "start":

        if args.modulo == "recon":
            ParserRecon()

        elif args.modulo == "exploitdb":
            ExploitDB_Parser()
    
    if args.comando == "list":

        if args.type == "payloads":
            pathway = pathlib.Path("payloads")
            

            print("-=" * 20)
            print(red)
            for file in pathway.rglob("*.py"):
                print(file)
            for f in pathway.iterdir():
                if f.is_file():
                    print(f)
            print(limit)
            print("-=" * 20)

        elif args.type == "modules":
            pathway = pathlib.Path("modules")

            print("-=" * 20)
            print(red)
            for file in pathway.iterdir():
                print(file)
            print(limit)
            print("-=" * 20)

    if args.comando == "use":
        if args.attack == "exploit":
            attack_parser()


        
