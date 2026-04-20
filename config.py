import argparse

def arguments(command):
    parser = argparse.ArgumentParser(description="Protus parser")

    parser.add_argument('comando', choices=['show'])
    

    args = parser.parse_args(command.split())

    if args.comando == 'show':
        print("""
Protus, The Framework for Pentest
Version: 0.1v
Features: A framework for pentest
""")
    else:
        print()
        
