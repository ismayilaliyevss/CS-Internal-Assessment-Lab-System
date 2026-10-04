from login_window import open_login_window
from main_menu import open_main_menu

open_login_window(open_main_menu)           # So, here we are just connecting login_window with main_menu, whenever open_login_window gets a real username-password pair, it will go the open_main_menu (on_success is the same function with open_main_menu, it is just in login_window.py file)