#!/usr/bin/env python3

import sqlite3

from sqlite3 import Error
from datetime import datetime
import functions

database = r"/home/sean_local/NetScan/netscan/sqlite_netscan.db"

def connect():
    conn = None
    conn = sqlite3.connect(database)
    if conn is not None:
        return conn

def get_scan_id():
    conn = connect()
    cur = conn.cursor()
    sql_find_max_id = """SELECT MAX(scan_id) FROM scans"""
    try:
        cur.execute(sql_find_max_id)
        max_id = cur.fetchall()
        for row in max_id:
            if row[0] is not None:
                scan_id = row[0] + 1
            else:
                scan_id = 1
    except Error as e:
        print("[-] Error: get_scan_id function.")
        print(e)
        scan_id = 0
        

    return scan_id

def get_hst_id():
    conn = connect()
    cur = conn.cursor()
    sql_find_max_id = """SELECT MAX(hst_id) FROM hosts"""
    try:
        cur.execute(sql_find_max_id)
        max_id = cur.fetchall()
        for row in max_id:
            if row[0] is not None:
                hst_id = row[0] + 1
            else:
                hst_id = 1
    except Error as e:
        print(e)
        hst_id = 0 
    return hst_id

def add_host(hst_id,scan_id,ip_addr,mac_addr,date_time):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""INSERT INTO hosts (hst_id,scan_id,ip_addr,mac_addr,date_time) values(?,?,?,?,?)""",(hst_id,scan_id,ip_addr,mac_addr,date_time))
        conn.commit()
        conn.close()
        print("[+] SCAN ID " + str(scan_id) + ": Host " + ip_addr + " with MAC " + mac_addr + " at " + date_time)
    except Error as e:
        print("[-] Error adding host to hosts table.")

def add_to_scans_table(scan_id, date_time, target_net, duration):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""SELECT DISTINCT(mac_addr) FROM hosts WHERE scan_id = ?""",(scan_id,))
        num_hosts = cur.fetchall()
        num_hosts = len(num_hosts)
        print("[+] Total hosts discovered - " + str(num_hosts))
        cur.execute("""REPLACE INTO scans (scan_id,date_time,num_hosts,target_net,duration) VALUES(?,?,?,?,?)""",(scan_id,date_time,num_hosts,target_net,duration))
        conn.commit()
        conn.close()
        print("[+] Added Scan to scan table.")
    except Error as e:
        print("[-] Error adding scan to scans table.")
        print(e)

def get_mac_list_found(scan_id, mac_addr):
    conn = connect()
    cur = conn.cursor()
    scan_id = str(scan_id)
    new = True
    mac_list = [0]
    try:
        cur.execute("""SELECT DISTINCT(mac_addr) FROM hosts WHERE scan_id = ?""",(scan_id,))
        mac_list = cur.fetchall()       
        
        mac_list = functions.create_mac_list_from_sql(mac_list)

        if mac_list:
            if mac_addr in mac_list:
                new = False
            else:
                new = True

    except Error as e:
        print("[-] Error getting found MAC address list.")
        print(e)

    return new

def add_known_host(mac_addr):

    conn = connect()
    cur = conn.cursor()
    custom_name = "Placeholder Name"
    group_id = 0

    hst_id = get_known_hst_id()

    try:
        cur.execute("""INSERT INTO known_hosts (hst_id,mac_addr,custom_name,group_id) VALUES(?,?,?,?)""",(hst_id,mac_addr,custom_name,group_id))
        conn.commit()
        conn.close()
        print("[+] Host " + mac_addr + " added to known hosts list.")
    except Error as e:
        print("[-] Error adding host " + mac_addr + " to known hosts list.")
        print(e)

def add_known_host_by_host_id(host_id):

    conn = connect()
    cur = conn.cursor()

    custom_name = "N/A"
    group_id = 0
    mac_addr = "N/A"
    known_hst_id = get_known_hst_id()

    try:
        cur.execute("""SELECT mac_addr FROM hosts WHERE hst_id = ?;""",(host_id,))
        mac_addr = cur.fetchone()
        mac_addr = mac_addr[0]
        try:
            cur.execute("""INSERT INTO known_hosts (hst_id, mac_addr, custom_name, group_id) VALUES (?,?,?,?);""",(known_hst_id, mac_addr, custom_name, group_id,))
            print("[+] Added " + mac_addr + " to known hosts.")
            conn.commit()
            conn.close()
        except Error as e:
            print("[-] Unable to add mac to known hosts list. db_config.add_known_host_by_host_id")
            print(e)
    except Error as e:
        print("[-] Unable to get MAC address from hosts table by host id. db_config.add_known_host_by_host_id()")
        print(e)

def del_known_host(hst_id):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""DELETE FROM known_hosts WHERE hst_id = ?""",(hst_id,))
        conn.commit()
        conn.close()
        print("[+] Host successfully deleted from known hosts list.")
    except Error as e:
        print("[-] Error deleting host from known host list.")
        print(e)

def get_known_host_list(group_id):
    conn = connect()
    cur = conn.cursor()
    if group_id is None:
        group_id = 0

    try:
        cur.execute("""SELECT * FROM known_hosts WHERE group_id = ?""",(group_id,))
        known_hosts_list = cur.fetchall()
        return known_hosts_list
        print("[+] Retrieved known host list for group id " + str(group_id) + ".")
    except Error as e:
        print("[-] Error retrieving known host list group id " + str(group_id) + ".")

def get_known_hst_id():
    conn = connect()
    cur = conn.cursor()
    sql_find_max_id = """SELECT MAX(hst_id) FROM known_hosts"""
    try:
        cur.execute(sql_find_max_id)
        max_id = cur.fetchall()
        for row in max_id:
            if row[0] is not None:
                hst_id = row[0] + 1
            else:
                hst_id = 1
    except Error as e:
        print(e)
        hst_id = 0 
    return hst_id

def get_hosts_from_scan(scan_id):
    conn = connect()
    cur = conn.cursor()

    hosts_from_scan = []
    scan_id = int(scan_id)
    
    try:
        cur.execute("""SELECT hst_id,mac_addr,ip_addr,date_time
                        FROM hosts
                        WHERE scan_id = ?;""",(scan_id,))
        hosts_from_scan = cur.fetchall()
        return hosts_from_scan
    except Error as e:
        print("[-] Unable to retrieve hosts from prior scan.")
        print(e)

def get_scans_list():
    conn = connect()
    cur = conn.cursor()

    sql_get_scans_list = """SELECT * from scans;"""

    try:
        cur.execute(sql_get_scans_list)
        scans_list = cur.fetchall()
        return scans_list
    except Error as e:
        print("[-] Unable to retrieve Scans list. db_config.get_scans_list()")
        print(e)

def get_scan_date(scan_id):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""SELECT date_time FROM hosts WHERE scan_id = ?;""",(scan_id,))
        scan_date = cur.fetchone()
        scan_date = scan_date[0]
        return scan_date
    except Error as e:
        print("[-] Error getting scan date. get_scan_date")
        print(e)

def get_known_host(host_id):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""SELECT * FROM known_hosts WHERE hst_id = ?;""",(host_id,))
        known_host = cur.fetchone()
        return known_host
    except Error as e:
        print("[-] Error getting known host. db_config.get_known_host()")
        print(e)

def update_known_host_name(host_id, new_name):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""UPDATE known_hosts SET custom_name = ? WHERE hst_id = ?;""",(new_name, host_id,))
        print("[+] Name updated to " + new_name)
        conn.commit()
        conn.close()
    except Error as e:
        print("[-] Error updating custom name for known host. db_config.update_known_host_name()")
        print(e)

def get_current_options():
    conn = connect()
    cur = conn.cursor()

    sql_get_current_options = """SELECT * FROM options
                                    WHERE opt_id = 0;"""

    try:
        cur.execute(sql_get_current_options)
        current_options = cur.fetchone()
    except Error as e:
        print("[-] Unable to retrieve current options.")
        print(e)
        current_options = ["N/A","N/A","N/A","N/A"]
    
    return current_options
    
def add_options_target_network(option):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""UPDATE options set target_network = ? WHERE opt_id = 0;""",(option,))
        print("[+] Added target network option.")
        conn.commit()
        conn.close()
    except Error as e:
        print("[-] Unable to add target network option.")
        print(e)

def add_options_duration(option):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""UPDATE options set duration = ? WHERE opt_id = 0;""",(option,))
        print("[+] Added duration option.")
        conn.commit()
        conn.close()
    except Error as e:
        print("[-] Unable to add duration option.")
        print(e)

def add_options_interval(option):
    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute("""UPDATE options set interval = ? WHERE opt_id = 0;""",(option,))
        print("[+] Added interval option.")
        conn.commit()
        conn.close()
    except Error as e:
        print("[-] Unable to add interval option.")
        print(e)

def get_unique_scan_ids():
    conn = connect()
    cur = conn.cursor()

    sql_get_unique_scan_ids="""SELECT DISTINCT(scan_id) FROM scans"""

    try:
        cur.execute(sql_get_unique_scan_ids)
        scan_ids = cur.fetchall()
    except Error as e:
        print("[-] Error getting list of scan ids. db_config.get_unique_scan_id()")
        print(e)

def compare_mac_to_known(mac_addr):
    conn = connect()
    cur = conn.cursor()

    known = False

    known_list = get_known_host_list(0)

    for host in known_list:
        if mac_addr == host[1]:
            known = True
            break

    return known