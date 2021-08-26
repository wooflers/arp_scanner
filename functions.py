#!/usr/bin/env python3

from datetime import datetime
from playsound import playsound
import time


def clean_sql1(sql_string):
    sql_string = sql_string.strip("(u',)")
    return sql_string

def clean_date1():
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")
    return date_time

def create_mac_list_from_sql(sql_list):
    mac_list = []
    for mac in sql_list:
        mac = str(mac)
        mac = mac.strip("(u',)")
        mac_list += [mac]
    return mac_list

def choose_host_from_scans_list():
    print ("choose_host_from_scans_list")

def compare_hosts_with_known(mac_addr):
    known_hosts = db_config.get_known_host_list()

    for host in known_hosts:
        print(host)

def unknown_alert():
    playsound('alert.wav')
