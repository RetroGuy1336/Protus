from scapy.all import *
import time

stealth_modes = {
    0: 0,
    1: 0.1,
    2: 0.3,
    3: 0.7,
    4: 1.5
}

services = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    3306: "MySQL",
    3389: "RDP",
    6379: "Redis",
    27017: "MongoDB"
}

class Module:
    name = "Protus Port Scanner"
    description = "A port scanner from the Protus Framework"

    def run(self, args):
        ports_ipv4 = []

        host = args.host
        first_port = args.Fp
        last_port = args.Lp
        stealth = args.St

        for port in range(first_port, last_port + 1):
            # Create a SYN packet for the target port
            pacote = IP(dst=host) / TCP(dport=port, flags="S")
            # Send the packet and wait for a response
            resposta = sr1(pacote, timeout=1, verbose=0)

            if resposta is None:
                ports_ipv4.append(("[ ? ]", port, "Filtered"))

            elif resposta.haslayer(TCP):
                if resposta[TCP].flags == "SA":
                    service_name = services.get(port, "Unknown")
                    ports_ipv4.append(("[ + ] ", port, "Open", service_name))

                    send(IP(dst=host)/TCP(dport=port, flags="R"), verbose=0)

            else:
                ports_ipv4.append((port, "Unknown"))

            time.sleep(stealth_modes[stealth])

        for status, port, status2, service in ports_ipv4:
            print(f"{status} {port} is {status2}  - {service}")
