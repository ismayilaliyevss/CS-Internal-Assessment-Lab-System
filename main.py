from login_window import open_login_window
from main_menu import open_main_menu
from db import create_tables, load_all_patients

create_tables()
hash_table = load_all_patients()            # the hash table gets loaded once the program starts

def start_main_menu(staff):                 # login screen only passes the staff
    open_main_menu(staff, hash_table)       # so we add hash_table before calling open_main_menu - as open_main_menu needs hash table also to function

open_login_window(start_main_menu)           # So, here we are just connecting login_window with main_menu, whenever open_login_window gets a real username-password pair, it will go the open_main_menu (on_success is the same function with open_main_menu, it is just in login_window.py file)