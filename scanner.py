#!/usr/bin/env python3

import scapy.all as scapy

import db_config
import functions

database = r"/home/sean_local/NetScan/netscan/sqlite_netscan.db"

def scan(ip, scan_id):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=3, verbose=False)[0]
            
    for element in answered_list:
        conn = db_config.connect()
        cur = conn.cursor()

        date_time = functions.clean_date1()
        hst_id = db_config.get_hst_id()
        ip_addr = element[1].psrc
        mac_addr = element[1].hwsrc

        new_mac = db_config.get_mac_list_found(scan_id, mac_addr)

        if new_mac is True:
            db_config.add_host(hst_id,scan_id,ip_addr,mac_addr,date_time)

        conn.close()