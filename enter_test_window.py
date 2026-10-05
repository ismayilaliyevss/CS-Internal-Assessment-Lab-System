import tkinter as tk
from tkinter import ttk
from datetime import date, datetime
from test_entry import enter_test_result

LABEL_FONT = ("Arial", 13)
BUTTON_FONT = ("Arial", 12)
ENTRY_FONT = ("Arial", 13)

TEST_TYPES = ["HbA1c", "Lipid", "CBC"]

def open_enter_test_window(staff, hash_table, back_to_menu):
    window = tk.Tk()
    window.title("HashLab - Enter Test Result")
    window.geometry("420x600")

    tk.Label(window, text=f"Logged in as: {staff.username} ({staff.staff_id}) - {staff.role}", font=LABEL_FONT).pack(pady=(15, 5))

    tk.Label(window, text="Patient phone number (10 digits)", font=LABEL_FONT).pack(pady=(10,0))
    phone_entry = tk.Entry(window, font=ENTRY_FONT)
    phone_entry.pack()

    tk.Label(window, text="Test type", font=LABEL_FONT).pack(pady=(10,0))
    type_box = ttk.Combobox(window, values=TEST_TYPES, state="readonly", font=ENTRY_FONT)       # readonly is basically only picks from the list, no typing allowed
    type_box.current(0)             # this means that it will start with the first item in the list - HbA1c
    type_box.pack()

    tk.Label(window, text="Result value", font=LABEL_FONT).pack(pady=(10, 0))
    value_entry = tk.Entry(window, font=ENTRY_FONT)
    value_entry.pack()

    tk.Label(window, text="Test date (DD/MM/YYYY)", font=LABEL_FONT).pack(pady=(10,0))
    date_entry = tk.Entry(window, font=ENTRY_FONT)
    date_entry.insert(0, date.today().strftime("%d/%m/%Y"))     # as in most cases doctors just enter the tests happened the same day, so the date is just prefilled with today's date
    date_entry.pack()

    message_label = tk.Label(window, text="", font=LABEL_FONT, fg="red", wraplength=380)
    classification_label = tk.Label(window, text="", font=LABEL_FONT)
    due_label = tk.Label(window, text="", font=LABEL_FONT)

    def attempt_save():
        phone = phone_entry.get().strip()
        test_type = type_box.get()
        value_text = value_entry.get().strip()
        date_text = date_entry.get().strip()

        classification_label.config(text="")    # cleaning the previous result
        due_label.config(text="")

        if not phone.isdigit() or len(phone) != 10:
            message_label.config(text="Error: phone number must be exactly 10 digits", fg="red")
            return

        try:
            result_value = float(value_text)
        except ValueError:
            message_label.config(text="Error: result value must be a number", fg="red")
            return
        if result_value <= 0:
            message_label.config(text="Error: result value must be greater than 0", fg="red")
            return 

        try:
            test_date = datetime.strptime(date_text, "%d/%m/%Y").date()
        except ValueError:
            message_label.config(text="Error: date must be a real date written as DD/MM/YYYY", fg="red")
            return

        if test_date > date.today():
            message_label.config(text="Error: test date cannot be in the future", fg="red")
            return
        result = enter_test_result(phone, test_type, result_value, test_date, hash_table, staff.staff_id)

        if isinstance(result, str):
            message_label.config(text=result, fg="red")
        else:
            message_label.config(text="Result saved", fg="green")
            classification_label.config(text=f"Classification: {result.classification.capitalize()}")
            due_label.config(text=f"Next due: {result.next_due_date.strftime('%d/%m/%Y')}")
            value_entry.delete(0, tk.END)           # cleares everything except the phone - doctor can enter several tests for the same patient 

    def go_back():
        window.destroy()
        back_to_menu(staff)

    tk.Button(window, text="Save result", command=attempt_save, font=BUTTON_FONT, width=20).pack(pady=10)
    message_label.pack()
    classification_label.pack(pady=(10, 0))
    due_label.pack(pady=(5, 0))
    tk.Button(window, text="Back to Menu", command=go_back, font=BUTTON_FONT, width = 20).pack(pady=(20, 0))

    window.mainloop()
