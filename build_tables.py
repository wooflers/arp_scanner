#!/usr/bin/env python3

import sqlite3
from sqlite3 import Error

database = r"/home/sean_local/NetScan/netscan/sqlite_netscan.db"

def connect():
    conn = None
    conn = sqlite3.connect(database)
    if conn is not None:
        return conn

def create_table(conn, create_table_sql):

    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(create_table_sql)
    except Error as e:
        print("[-] Error connecting to SQLite database.")
        print(e)


def build_hosts_table():

    conn=connect()

    sql_create_hosts_table = """CREATE TABLE IF NOT EXISTS hosts (
                                    hst_id int PRIMARY KEY NOT NULL,
                                    scan_id int NOT NULL,
                                    ip_addr text NOT NULL,
                                    mac_addr text NOT NULL,
                                    date_time text NOT NULL
                                );"""

    print("[+] Building hosts table.")

    if conn is not None:
        try:
            create_table(conn, sql_create_hosts_table)
            print("[+] Successfully created hosts table.")
        except Error as e:
            print("[-] Failed to create hosts table.")
            print(e)
        conn.commit()
        conn.close()     

    else:
        print("[-] Error. Cannot create the database connection to buld hosts table.")

def build_scans_table():
    conn=connect()

    sql_create_scans_table = """ CREATE TABLE IF NOT EXISTS scans (
                                    scan_id int PRIMARY KEY NOT NULL,
                                    date_time text NOT NULL,
                                    num_hosts int NOT NULL,
                                    target_net text NOT NULL,
                                    duration int NOT NULL
                                );"""
    
    print("[+] Building scans table.")

    if conn is not None:
        try:    
            create_table(conn, sql_create_scans_table)
            print("[+] Successfully created scans table.")
        except Error as e:
            print("[-] Failed to create scans table.")
            print(e)
        conn.commit()
        conn.close()
    else:
        print("[-] Error. Cannot create the database connection to buld scans table.")

def build_known_hosts_table():

    conn=connect()

    sql_create_known_hosts_table = """ CREATE TABLE IF NOT EXISTS known_hosts (
                                    hst_id int NOT NULL,
                                    mac_addr text NOT NULL,
                                    custom_name text,
                                    group_id int NOT NULL
                                );"""
    
    print("[+] Building known hosts table.")

    if conn is not None:
        try:    
            create_table(conn, sql_create_known_hosts_table)
            print("[+] Successfully created known hosts table.")
        except Error as e:
            print("[-] Failed to create known hosts table.")
            print(e)
        conn.commit()
        conn.close()
    else:
        print("[-] Error. Cannot create the database connection to buld known hosts table.")

def build_scan_settings_table():
    conn=connect()

    sql_create_scan_settings_table = """ CREATE TABLE IF NOT EXISTS scan_settings (
                                    opt_id int NOT NULL,
                                    target_network text NOT NULL,
                                    duration int NOT NULL
                                );"""
  
    print("[+] Building scan_settings table.")

    if conn is not None:
        try:    
            create_table(conn, sql_create_scan_settings_table)
            print("[+] Successfully created scan_settings table.")
        except Error as e:
            print("[-] Failed to create scan_settings table.")
            print(e)
        conn.commit()
        conn.close()
    else:
        print("[-] Error. Cannot create the database connection to buld options table.")

def build_options_table():
    conn = connect()
    cur = conn.cursor()

    sql_create_options_table = """ CREATE TABLE IF NOT EXISTS options (
                                    opt_id int NOT NULL,
                                    target_network text NOT NULL,
                                    duration int NOT NULL,
                                    interval int NOT NULL,
                                    db_ver text NOT NULL
                                );"""
    sql_default_options_table = """INSERT INTO options (opt_id, target_network, duration, interval, db_ver) VALUES (0, "UNDEFINED", 10, 5, "v0.0.8")"""
    
    print("[+] Building options table.")

    if conn is not None:
        try:    
            create_table(conn, sql_create_options_table)
            cur.execute(sql_default_options_table)
            print("[+] Successfully created options table.")
        except Error as e:
            print("[-] Failed to create options table.")
            print(e)
        conn.commit()
        conn.close()
    else:
        print("[-] Error. Cannot create the database connection to buld options table.")


def rebuild_scans_table():

    conn = connect()
    cur = conn.cursor()

    sql_clear_scans_table = """DROP TABLE scans;"""

    print("[+] Deleting scans table")
    try:
        cur.execute(sql_clear_scans_table)
        print("[+] Deleted scans table.")
        conn.commit()
        conn.close()
    except Error as e:
        print("[-] Error deleteing scans table.")
        print (e)
    build_scans_table()

def rebuild_hosts_table():
    conn = connect()
    cur = conn.cursor()

    sql_delete_hosts_table = """DROP TABLE hosts;"""

    print("[+] Deleting hosts table")

    try:
        cur.execute(sql_delete_hosts_table)
        print("[+] Deleted hosts table.")
        conn.commit()
        conn.close()
    except Error as e:
        print("[-] Error deleteing hosts table.")
        print (e)
    build_hosts_table()

def rebuild_known_hosts_table():
    conn = connect()
    cur = conn.cursor()

    sql_delete_known_hosts_table = """DROP TABLE known_hosts;"""

    print("[+] Deleting known hosts table")

    try:
        cur.execute(sql_delete_known_hosts_table)
        print("[+] Deleted known hosts table.")
        conn.commit()
        conn.close()
    except Error as e:
        print("[-] Error deleteing known hosts table.")
        print (e)
    build_known_hosts_table()

def rebuild_scan_settings_table():

    conn = connect()
    cur = conn.cursor()

    sql_delete_scan_settings_table = """DROP TABLE scan_settings;"""

    print("[+] Deleting scan_settings table.")

    try:
        cur.execute(sql_delete_scan_settings_table)
        print("[+] Deleted scan_settings table.")
        conn.commit()
        conn.close()
    except Error as e:
        print("[-] Error deleteing scan_settings table.")
        print (e)
    build_scan_settings_table()

def rebuild_options_table():
    conn = connect()
    cur = conn.cursor()

    sql_delete_options_table = """DROP TABLE options;"""

    print("[+] Deleting options table.")

    try:
        cur.execute(sql_delete_options_table)
        print("[+] Deleted options table.")
        conn.commit()
        conn.close()
    except Error as e:
        print("[-] Error deleteing options table.")
        print (e)
    build_options_table()