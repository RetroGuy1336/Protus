import argparse
import os
import shlex
from modules.portscanner import scanner

def main():
    os.system('clear')
    print("Starting the Protus Scanner... ")

    print("""
    Please, input the host to scan, first port, last port and the stealth mode
    Read the arguments below to realize the scan:
    ---------------------------------------------
    scan = Defines the host to be scanned
    -Fp = Defines the first port to be scanned
    -Lp = Defines the last port to be scanned
    -St = Defines the Stealth mode (0-Agressive | 5-Stealth)
    ==============================================""")

    user = input("PTS_Scanner >> ")
    scannerparser(user)

def scannerparser(user_input):
    parser = argparse.ArgumentParser(prog="Protus Scanner")
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan = subparsers.add_parser("scan")

    scan.add_argument("host")
    scan.add_argument("-Fp", type=int, required=True)
    scan.add_argument("-Lp", type=int, required=True)
    scan.add_argument("-St", type=int, choices=range(0,6), required=True)

    try:
        args = parser.parse_args(shlex.split(user_input))
    except SystemExit:
        # impede o programa de fechar se o usuário errar comando
        return

    if args.command == "scan":
        scanner(args)