import scapy.all as scapy
from scapy_http import http
import argparse

def get_interface():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i','--interface', dest="Interface", help="Specify an interface to capture packets from")
    options = parser.parse_args()
    
    if not  options.interface:
        parser.error('[-] please specify a value for the interface, enter --help for more info')
    
    return options

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        print(packet.show())


options = get_interface()
sniff(options.interface)