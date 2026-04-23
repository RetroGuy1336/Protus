#                    Welcome to Protus!
#
#   ░█████████                         ░██                          
#   ░██     ░██                        ░██                          
#   ░██     ░██ ░██░████  ░███████  ░████████ ░██    ░██  ░███████  
#   ░█████████  ░███     ░██    ░██    ░██    ░██    ░██ ░██        
#   ░██         ░██      ░██    ░██    ░██    ░██    ░██  ░███████  
#   ░██         ░██      ░██    ░██    ░██    ░██   ░███        ░██ 
#   ░██         ░██       ░███████      ░████  ░█████░██  ░███████  
#
#                   Developed by RetroGuy1336

from banners import random_banners
from core.config import arguments
import os

red = '\033[1;31m'
blue = '\033[1;34m'
limit = '\033[m'

def main():
    os.system('clear')
    if os.geteuid() != 0:
        print("Execute with sudo!")
        exit()
    while True:
        print(red)
        random_banners()
        print(limit)
        print("""
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
[ + ]     --[   Protus, Programmable Recon & Offensive Toolkit for Unified Systems   ]
[ + ] --  -=[   We have only a Port Scanner and a DNS Lookup for attacks D:          ]
[ + ] -  --=[   ---------------Developed by RetroGuy1336-----------------            ]""")
        user = input(blue + "pts >> " + limit)
        arguments(user)


if __name__ == "__main__":
    main()