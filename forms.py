#!/usr/bin/env python3

import reports
import db_config
import net_functions
import functions

header = """
    ============================
    re-Netscan
    Wooflers
    v0.0.8
    ============================"""


def main_menu():
    current_options = db_config.get_current_options()

    main_menu_form = """
    SCAN
    Current scan settings:

    Selected Network: {target_network}
    Scan duration: {duration}
    Scan Interval: {interval}

    ============================
    Choose an option --
    1) Scan
    2) Known hosts list
    3) View scan results
    4) Set scan settings
    5) Database options
    h) Help
    x) Exit
    ============================
    """.format(target_network = current_options[1], duration = current_options[2], interval = current_options[3])

    print(header)
    print(main_menu_form)
    option = input("Option : ")
    return option


def scan_form():
    current_options = db_config.get_current_options()

    target_network = current_options[1]
    duration = current_options[2]
    interval = current_options[3]
    scan_id = db_config.get_scan_id()
    date_time = functions.clean_date1()

    scan_form = """
    MAIN MENU
    Current scan settings:

    Selected Network: {target_network}
    Scan duration: {duration}
    Scan Interval: {interval}

    ============================
    Scanning...
    ============================
    """.format(target_network = target_network, duration = duration, interval = interval)

    print(header)
    print(scan_form)
    
    try:
        net_functions.scan_looper(interval, duration, target_network, scan_id)
        db_config.add_to_scans_table(scan_id, date_time, target_network, duration)
    except KeyboardInterrupt:
        print("[-] Scan stopped due to keyboard interrupt.")

    print("""

    """)
    

def known_host_form_0():

    known_host_form_0="""
    KNOWN HOSTS
    
    ============================
    Choose an option --
    1) Add host to known hosts list
    2) Delete host from known hosts list
    3) View known hosts list
    4) Add/Change known host name
    m) Main Menu
    ============================
    """

    print(header)
    print(known_host_form_0)

    option = input("Option : ")
    return option

    print("""
    
    """)

def add_known_host_0():

    add_known_host_form_0="""
    ADD KNOWN HOST
    SELECT SCAN
    ============================
    Select a Scan ID to view hosts or type m for Main Menu

    ScanID     Network      Hosts          Time
    -----------------------------------------------------
    ============================
    """

    print(header)
    print(add_known_host_form_0)

    reports.display_scan_list1()

    print("""
    
    """)

    scan_id = input("Scan ID : ")
    return scan_id
    
def add_known_host_1(scan_id):


    add_known_host_form_1="""
    ADD KNOWN HOST
    SELECT HOST
    ============================
    Select HostID of Host to add to known list.
    Enter m to return to main menu.

    MAC                HostID      
    ----------------------------"""

    print(header)
    print(add_known_host_form_1)

    reports.display_hosts_list2(scan_id)

    print("""
    
    """)

    while True:
        host_id = input("Host ID : ")
        if host_id == 'm':
            break
        else:
            host_list = db_config.get_hosts_from_scan(scan_id)
            db_config.add_known_host_by_host_id(host_id)

def view_known_hosts():

    view_known_host_form="""
    KNOWN HOSTS LISTS
    ============================
    Current list of known hosts.

    MAC                  Custom Name
    ---------------------------------------------"""

    print(header)
    print(view_known_host_form)

    reports.display_known_hosts_list1(0)

    input("""
    Press ENTER to return to previous menu
    """)

def delete_known_host():

    view_known_host_form="""
    KNOWN HOSTS LISTS
    ============================
    Current list of known hosts.
    Enter ID of known host to delete.

    MAC                HostID      
    ----------------------------"""

    print(header)
    print(view_known_host_form)

    reports.display_known_hosts_list2(0)

    print("""
    
    """)

    while True:
        host_id = input("Host ID : ")
        if host_id is None:
            print("[-] Select a host ID.")
        elif host_id == 'm':
            break
        else:
            db_config.del_known_host(host_id)

def name_known_host():
    view_known_host_form="""
    KNOWN HOSTS LISTS
    ============================
    Current list of known hosts.
    Enter HostID to change Custom Name.
    Enter m to return to menu.

    MAC                HostID            Custom Name        
    --------------------------------------------------"""

    print(header)
    print(view_known_host_form)

    reports.display_known_hosts_list2(0)

    print("""
    
    """)
    try:
        while True:
            option = input("Option : ")
            if option == 'm':
                break
            else:
                current_name = db_config.get_known_host(option)
                current_name = current_name[2]
                print("[+] Current Name : " + current_name)
                new_name = input("[o] New Name : ")
                db_config.update_known_host_name(option, new_name)
    except TypeError:
        print("[-] TypeError. Please enter a valid option.")


def view_scan_results_1():

    view_scan_results_1_form = """
    VIEW SCAN RESULTS
    SELECT SCAN
    ============================
    Select a Scan ID to view results or type m for Main Menu

    ScanID     Network      Hosts          Time
    -----------------------------------------------------
    """

    print(header)
    print(view_scan_results_1_form)

    reports.display_scan_list1()

    print("""
    
    """)
    
    while True:
        scan_id = input("Scan ID : ")
        try:
            if scan_id == 'm':
                break
            else:
                return scan_id
        except TypeError:
            print("[-] TypeError. Enter a valid option.")   

def view_scan_results_2(scan_id):

    date_time = db_config.get_scan_date(scan_id)

    view_scan_results_2_form = """
    ============================
    VIEW SCAN RESULTS
    SCAN {scan}
    DATE {date}
    RESULTS
    ============================

    Known     MAC                     IP                Name
    --------------------------------------------------------------
    """.format(scan = scan_id, date = date_time) 

    print(header)
    print(view_scan_results_2_form)
    print(reports.display_hosts_list1(scan_id))

    input("""
    Press ENTER to return to previous menu
    """)
    

def scan_settings_0():
    current_options = db_config.get_current_options()

    scan_settings_form_1 = """
    OPTIONS
    Current scan settings:

    Selected Network: {target_network}
    Scan Duration: {duration}
    Scan Interval: {interval}

    ============================
    Choose an option --
    1) Choose target network
    2) Change scanning duration
    3) Choose Scan interval
    m) Main Menu
    ============================
    """.format(target_network = current_options[1], duration = current_options[2],  interval = current_options[3], version = ver)

    print(header)
    print(scan_settings_form_1)

    option = input("Option : ")
    return option

def scan_settings_1():
    current_options = db_config.get_current_options()

    scan_settings_form_1 = """
    OPTIONS - SET NETWORK
    Current scan settings:

    Selected Network: {target_network}
    Scan Duration: {duration}
    Scan Interval: {interval}

    ============================
    Type the network address to scan in CIDR format.
    ex. 192.168.0.1/24

    m) Main Menu
    ============================
    """.format(target_network = current_options[1], duration = current_options[2],  interval = current_options[3])

    print(header)
    print(scan_settings_form_1)

    option = str(input("Option : "))

    if option == 'm':
        print("Main Menu")
        return option
    else:
        print(option)
        db_config.add_options_target_network(option)

def scan_settings_2():
    current_options = db_config.get_current_options()

    scan_settings_form_2 = """
    OPTIONS - SET DURATION
    Current scan settings:

    Selected Network: {target_network}
    Scan Duration: {duration}
    Scan Interval: {interval}

    ============================
    Type how long you want the scan in seconds and press ENTER.

    m) Main Menu
    ============================
    """.format(target_network = current_options[1], duration = current_options[2],  interval = current_options[3])

    print(header)
    print(scan_settings_form_2)

    option = input("Option : ")

    if option == 'm':
        print("Main Menu")
        return option
    else:
        option = int(option)
        db_config.add_options_duration(option)

def scan_settings_3():
    current_options = db_config.get_current_options()

    scan_settings_form_3 = """
    OPTIONS - INTERVAL
    Current scan settings:

    Selected Network: {target_network}
    Scan Duration: {duration}
    Scan Interval: {interval}

    ============================
    Type the interval between scans in sconds.

    m) Main Menu
    ============================
    """.format(target_network = current_options[1], duration = current_options[2], interval = current_options[3])

    print(header)
    print(scan_settings_form_3)

    option = input("Option : ")

    if option == 'm':
        print("Main Menu")
        return option
    else:
        option = int(option)
        db_config.add_options_interval(option)


def database_options():

    database_options_form = """
    DATABASE OPTIONS
    ============================
    Choose an option --
    1) Rebuild 'hosts' table.
    2) Rebuild 'scans' table.
    3) Rebuild 'known hosts' table.
    4) Rebuild 'scan settings' table.
    5) Rebuild 'options' table.
    6) Rebuild all tables.
    m) Main Menu

    """

    print(header)
    print(database_options_form)

    option = input("Option : ")
    return option


def show_help():
    help_file = reports.get_help_file()

    show_help_form="""
    HELP
    ============================
    """

    print(header)
    print(show_help_form)
    print(help_file)

    print("""
    
    """)

    input("""
    Press ENTER to return to previous menu
    """)
