import tkinter as tk
from register_patient_window import open_register_patient_window

LABEL_FONT = ("Arial", 13)          # firstly, I was writing them by hand each time, but whenever I tried to change it - it became so hard to change for each text, so I just created variables - make it easier to modify
BUTTON_FONT = ("Arial", 12)
ENTRY_FONT = ("Arial", 13)

def open_main_menu(staff, hash_table):          # staff is just StuffMember object login_window.py hands over 
    window = tk.Tk()
    window.title("Hashlab - Main Menu")
    window.geometry("380x400")

    tk.Label(window, text = f"Logged in as: {staff.username} ({staff.staff_id}) - {staff.role}", font = LABEL_FONT).pack(pady=(20,15))

    def go_to_register(staff):
        window.destroy()
        def back_to_this_menu(staff):           # I am doing the same thing I did in main.py, as register passes only staff we are adding hash_table also
             open_main_menu(staff, hash_table)
        open_register_patient_window(staff, hash_table, back_to_this_menu)

    if staff.role == "Technician":
        tk.Button(window, text = "Register Patient", command = lambda: go_to_register(staff), width=25, font = BUTTON_FONT).pack(pady=7)     # Register Patient - it is for only Technician


    tk.Button(window, text = "Search / Edit Patient", width=25, font = BUTTON_FONT).pack(pady=7)    # Search / Edit Patient - is visible for both roles

    if staff.role == "Doctor":
            tk.Button(window, text = "Enter Test Result", width=25, font = BUTTON_FONT).pack(pady=7)     # Enter Test Result - it is for only Doctor

    tk.Button(window, text="Follow-Up Schedule", width=25, font = BUTTON_FONT).pack(pady=7)              # Follow-Up Schedule - is visible for both roles

    if staff.role == "Technician":
            tk.Button(window, text = "Generate Report", width=25, font = BUTTON_FONT).pack(pady=7)     # Generate Report - it is for only Technician

    def go_to_login():          # I added this function because if two different staff members try to use the same computer to login to their accounts, you would need to close the whole system and run it again
        window.destroy()        # but in this way, with Logout button, you would just press it to go back to the Login window
        from login_window import open_login_window
        def restart_menu(staff):
             open_main_menu(staff, hash_table)
        open_login_window(restart_menu)         # login window opens -> user gives correct username + password -> login window runs restart_menu(staff) -> restart_menu runs open_main_menu(staff, hash_table)

    tk.Button(window, text = "Logout", command = go_to_login, width=25, font = BUTTON_FONT).pack(pady=(20,0))

    window.mainloop()