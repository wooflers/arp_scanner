#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error
import db_config
import sys

database = r"/home/sean_local/NetScan/netscan/sqlite_netscan.db"

def connect():
    conn = None
    conn = sqlite3.connect(database)
    if conn is not None:
        return conn

def mac_report():
    conn = connect()
    if conn is not None:
        conn.row_factory = lambda cursor, row: row[0]
        cur = conn.cursor()

        sql_get_mac_report="""SELECT DISTINCT(mac_addr) FROM hosts;"""
        
        try:
            cur.execute(sql_get_mac_report)
            mac_report = cur.fetchall()
            print("Unique MAC addresses seen:")
            for mac in mac_report:
                print(mac)
        except Error as e:
            print("Unable to generate mac report.")
            print(e)

def scan_report():
    conn = connect()
    if conn is not None:
        conn.row_factory = lambda cursor, row: row[0]
        cur = conn.cursor()

        sql_get_scan_report_number="""SELECT DISTINCT(scan_id) FROM hosts;"""

        try:
            cur.execute(sql_get_scan_report_number)
            scan_num = cur.fetchall()
            num_scans = str(len(scan_num))
            print("Total number of scans: " + num_scans)
            print("Live hosts seen during each scan.")
            print("Scan #            Live Hosts")
            print("-----------------------------")
            for scan_id in scan_num:
                cur.execute("""SELECT DISTINCT(mac_addr) FROM hosts WHERE scan_id = ?""",(scan_id,))
                mac_count = cur.fetchall()

                print(str(scan_id) + "           -            " + str(len(mac_count)))
            
                
        except Error as e:
            print("Unable to generate scan report.")
            print(e)

def display_scan_list1():
    scans_list = db_config.get_scans_list()
    for scan in scans_list:
        scan_id = str(scan[0])
        date_time = scan[1]
        num_hosts = str(scan[2])
        target_network = scan[3]
        
        print("    " + scan_id + "      " + target_network + "    " + num_hosts + "     " + date_time)

def display_hosts_list1(scan_id):
    hosts_from_scan = db_config.get_hosts_from_scan(scan_id)
    for host in hosts_from_scan:
        known = " "
        mac_addr = host[1]
        ip_addr = host[2]
        is_known = db_config.compare_mac_to_known(mac_addr)
        if is_known is True:
            known = "X"
        

        print("    " + known + "    " + mac_addr + "       " + ip_addr)

def display_hosts_list2(scan_id):

    hosts_from_scan = db_config.get_hosts_from_scan(scan_id)
    for host in hosts_from_scan:
        hostid = str(host[0])
        mac_addr = host[1]
        ip_addr = host[2]

        print("    " + mac_addr + "    " + hostid)

def display_known_hosts_list1(group_id):
    
    known_hosts_list = db_config.get_known_host_list(group_id)

    for host in known_hosts_list:
        hst_id = host[0]
        mac_addr = host[1]
        custom_name = host[2]
        group_id = host[3]

        print("    " + mac_addr + "    " + custom_name)

def display_known_hosts_list2(group_id):
    
    known_hosts_list = db_config.get_known_host_list(group_id)

    for host in known_hosts_list:
        hst_id = str(host[0])
        mac_addr = host[1]
        custom_name = host[2]
        group_id = host[3]

        print("    " + mac_addr + "    " + hst_id + "    " + custom_name)

def get_help_file():

    help_file = open('help.txt', 'r')
    help_file = help_file.read()
    return help_file