#!/usr/env/python3

import forms
import build_tables

def main():
    try:
        while True:
            main_menu_option = forms.main_menu()
            if main_menu_option == '1':
                while True:
                    forms.scan_form()
                    break
            if main_menu_option == '2':
                while True:
                    opt = forms.known_host_form_0()
                    print(opt)
                    if opt == '1':
                        sub_opt = forms.add_known_host_0()
                        if sub_opt == 'm':
                            break
                        else:
                            forms.add_known_host_1(sub_opt)
                            break
                    elif opt == '2':
                        forms.delete_known_host()
                        break
                    elif opt == '3':
                        forms.view_known_hosts()
                        break
                    elif opt == '4':
                        forms.name_known_host()
                    else:
                        break
            if main_menu_option == '3':           
                while True:
                    view_scan_opt = forms.view_scan_results_1()
                    if view_scan_opt == 'm':
                        break
                    else:
                        if view_scan_opt is None:
                            break
                        while True:
                            try:
                                forms.view_scan_results_2(view_scan_opt)
                                break
                            except TypeError:
                                print("[-] TypeError. Please enter a valid option.")
                                break
            if main_menu_option == '4':
                while True:
                    opt = forms.scan_settings_0()
                    if opt == 'm':
                        break
                    if opt == '1':
                        forms.scan_settings_1()
                    if opt == '2':
                        forms.scan_settings_2()
                    if opt == '3':
                        forms.scan_settings_3()
            if main_menu_option == '5':
                while True:
                    opt = forms.database_options()
                    if opt == '1':
                        build_tables.rebuild_hosts_table()
                    if opt == '2':
                        build_tables.rebuild_scans_table()
                    if opt == '3':
                        build_tables.rebuild_known_hosts_table()
                    if opt == '4':
                        build_tables.rebuild_scan_settings_table()
                    if opt == '5':
                        build_tables.rebuild_options_table()
                    if opt == '6':
                        build_tables.rebuild_hosts_table()
                        build_tables.rebuild_scans_table()
                        build_tables.rebuild_known_hosts_table()
                        build_tables.rebuild_scan_settings_table()
                        build_tables.rebuild_options_table()
                    if opt == 'm':
                        break
            if main_menu_option == 'h':
                forms.show_help()
                break
            if main_menu_option == 'x':
                exit()
    except KeyboardInterrupt:
        print("[-] Stopped due to KeyboardInterrupt.")
if __name__ == "__main__":
    while True:
        main()