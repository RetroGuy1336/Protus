import argparse

def arguments(command):
    parser = argparse.ArgumentParser(description="Protus parser")

    subparsers = parser.add_subparsers(dest='comando')
    show_parser = subparsers.add_parser('show')
    show_parser.add_argument('--more', action="store_true")

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
        
