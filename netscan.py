#!/usr/bin/env python3

import argparse
import time
from datetime import datetime

import scanner
import db_config
import reports
import build_tables
import functions


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--target",dest="target", help="Type the network in CIDR format that you'd like to scan")
    parser.add_argument("-l","--loopfor",dest="loopfor", help="Number of seconds to run scan. Default 15.")
    parser.add_argument("-r","--report",dest="report", help="Type the report to view. 'mac'")
    parser.add_argument("-sql","--sqlrebuild",dest="sqlrebuild",help="Specify table to clear. 1) all 2) scans 3) hosts 4) known_hosts")
    parser.add_argument("-a","--add",dest="add_host",help="Add a host to the known hosts list. '-a MAC_ADDR CUSTOM_NAME GROUP_NUMBER'", nargs='+')

    options = parser.parse_args()
    if not options:
        parser.error("[-] Please specify a network, use --help for more info.")
    return options

def check_args(args):

    if args.target is not None:
        scan_id = db_config.get_scan_id()
        time_end = time.time() + 15
        date_time = functions.clean_date1()
        if args.loopfor is not None:
            time_end = time.time() + int(args.loopfor)
            try:
                print("[+] Scanning for " + args.loopfor + " seconds.")
                while time.time() < time_end:
                    scanner.scan(args.target, scan_id)
                db_config.add_to_scans_table(scan_id, date_time, args.target, args.loopfor)
            except KeyboardInterrupt:
                print("[-] Scanning stopped due to keyboard inturrpt.")
                db_config.add_to_scans_table(scan_id, date_time, 0)
        try:
            print("[+] Scanning...")
            while time.time() < time_end:
                scanner.scan(args.target, scan_id)
                time.sleep(5)
            db_config.add_to_scans_table(scan_id, date_time, args.target, 15)
        except KeyboardInterrupt:
            print("[-] Scanning stopped due to keyboard inturrupt.")
            db_config.add_to_scans_table(scan_id, date_time, args.target, 0)
    elif args.report is not None:
        if args.report == "mac":
            reports.mac_report()
            print("[+] Printing mac report.")
        elif args.report == "scan":
            reports.scan_report()
            print("[+] Printing scan report.")
        else:
            print("[-] That is not a valid argument.")
    elif args.sqlrebuild is not None:
        if args.sqlrebuild == "all":
            build_tables.rebuild_hosts_table()
            build_tables.rebuild_scans_table()
            build_tables.rebuild_known_hosts_table()
            build_tables.rebuild_scan_settings_table()
            build_tables.rebuild_options_table()
        elif args.sqlrebuild == "hosts":
            build_tables.rebuild_hosts_table()
        elif args.sqlrebuild == "scans":
            build_tables.rebuild_scans_table()
        elif args.sqlrebuild == "known_hosts":
            build_tables.rebuild_known_hosts_table()
        else:
            print("[-] That is not a valid argument.")
    elif args.add_host is not None:
        db_config.add_known_host(args.add_host)
    else:
            print("[-] That is not a valid argument.")

args = get_arguments()
check_args(args)