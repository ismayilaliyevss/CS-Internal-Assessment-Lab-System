import tkinter as tk
from hash_table import HashTable

LABEL_FONT = ("Arial", 13)          # firstly, I was writing them by hand each time, but whenever I tried to change it - it became so hard to change for each text, so I just created variables - make it easier to modify
BUTTON_FONT = ("Arial", 12)
ENTRY_FONT = ("Arial", 13)

def open_register_patient_window(staff, hash_table, back_to_menu):
    window = tk.Tk()
    window.title("HashLab - Register Patient")
    window.geometry("380x380")

    tk.Label(window, text = "Name", font = LABEL_FONT).pack(pady=(15,0))
    name_entry = tk.Entry(window, font = ENTRY_FONT)
    name_entry.pack()

    tk.Label(window, text = "Surname", font=LABEL_FONT).pack(pady=(10,0))
    surname_entry = tk.Entry(window, font = ENTRY_FONT)
    surname_entry.pack()

    