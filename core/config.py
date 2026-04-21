import argparse
from modules.parserscanner import scannerparser

def arguments(command):
    parser = argparse.ArgumentParser(prog="Protus", description="Protus parser")

    subparsers = parser.add_subparsers(dest='comando')
    show_parser = subparsers.add_parser('show', help="It shows some things of Protus")
    show_parser.add_argument('--more', action="store_true")

    start_parser = subparsers.add_parser('start', help="It starts a module from Protus")
    start_sub = start_parser.add_subparsers(dest="modulo")
    scanner_parser = start_sub.add_parser("scanner")
    dns_parser = start_sub.add_parser("dnslookup")
    db_parser = start_sub.add_parser("dbsearch")

    try:
        args = parser.parse_args(command.split())
    except SystemExit:
        print("Command not found...")
        return
        
    if args.comando == 'show':
        print("""
Protus, The Framework for Pentest
Version: 0.1v
Description: Protus, The Framework for Pentest is a tool to assist offensive cybersecurity engineers in their work""")
        if args.more:
            print("No")

    if args.comando == "start":
        if args.modulo == "scanner":
            scannerparser()

        
