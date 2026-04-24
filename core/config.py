import argparse
from modules.recon.parser import ParserRecon
from modules.exploitdb.parser import ExploitDB_Parser
import os

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
            pathway = "payloads"

            files = os.listdir(pathway)
            print("-=" * 20)
            print(red)
            for file in files:
                print(file)
            print(limit)
            print("-=" * 20)

        elif args.type == "modules":
            pathway = "modules"

            files = os.listdir(pathway)
            print("-=" * 20)
            print(red)
            for file in files:
                print(file)
            print(limit)
            print("-=" * 20)


        
