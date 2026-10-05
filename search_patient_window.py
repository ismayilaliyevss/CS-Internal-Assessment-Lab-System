import tkinter as tk
 
LABEL_FONT = ("Arial", 13)
BUTTON_FONT = ("Arial", 12)
ENTRY_FONT = ("Arial", 13)
LIST_FONT = ("Arial", 12)

def open_search_patient_window(staff, hash_table, back_to_menu):
    window = tk.Tk()
    window.title("HashLab - Search Patient")
    window.geometry("440x600")

    tk.Label(window, text = f"Logged in as: {staff.username} ({staff.staff_id}) - {staff.role}", font=LABEL_FONT).pack(pady=(15, 5))
    tk.Label(window, text = "Search by phone number (10 digits)", font=LABEL_FONT).pack(pady=(10, 0))
    phone_entry = tk.Entry(window, font=ENTRY_FONT)
    phone_entry.pack()

    message_label = tk.Label(window, text="", font=LABEL_FONT, fg="red", wraplength=400)
    
    name_label = tk.Label(window, text="Name: -", font=LABEL_FONT)
    surname_label = tk.Label(window, text="Surname: -", font=LABEL_FONT)

    if staff.role == "Technician":
        visits_label = tk.Label(window, text="Visit count: -", font=LABEL_FONT)
        discount_label = tk.Label(window, text="Discount: -", font=LABEL_FONT)

    if staff.role == "Doctor":
            history_title = tk.Label(window, text="Test history", font=LABEL_FONT)
            history_listbox = tk.Listbox(window, font=LIST_FONT, width=45, height=8)

    def clear_results():
        name_label.config(text="Name: -")
        surname_label.config(text="Surname: -")

        if staff.role == "Technician":
            visits_label.config(text="Visit count: -") 
            discount_label.config(text="Discount: -")

        if staff.role == "Doctor":
            history_listbox.delete(0, tk.END)

    def attempt_search():
        phone = phone_entry.get().strip()

        if not phone.isdigit() or len(phone) !=10:
            clear_results()
            message_label.config(text="Error: phone number must be exactly 10 digits")
            return

        patient = hash_table.search(phone)  # using the hash searching here also
        if patient is None:
            clear_results()
            message_label.config(text="Patient not found")
            return

        message_label.config(text="")       # if the patient found we are removing the old error messages
        name_label.config(text=f"Name: {patient.name}")
        surname_label.config(text=f"Surname: {patient.surname}")

        if staff.role == "Technician":
            visits_label.config(text = f"Visit count: {patient.visit_count}")
            discount_label.config(text=f"Discount: {round(patient.get_discount() * 100)}%")

        if staff.role == "Doctor":
            history_listbox.delete(0, tk.END)

            if len(patient.tests) == 0:
                history_listbox.insert(tk.END, "No test history yet")
            newest_first = sorted(patient.tests, key=lambda test: test.test_date, reverse=True)

            for test in newest_first:
                line = f"{test.test_type} - {test.result_value} - {test.classification.capitalize()} - {test.test_date.strftime('%d/%m/%Y')}"    
                history_listbox.insert(tk.END, line)

    def go_back():
        window.destroy()
        back_to_menu(staff)

    tk.Button(window, text="Search", command=attempt_search, font=BUTTON_FONT, width=20).pack(pady=8)
    message_label.pack()
    name_label.pack(pady=(10, 0))
    surname_label.pack(pady=(5,0))
    if staff.role == "Technician":
        visits_label.pack(pady=(5, 0))
        discount_label.pack(pady=(5, 0))

    if staff.role == "Doctor":
            history_title.pack(pady=(15, 0))
            history_listbox.pack()

    tk.Button(window, text="Back to Menu", command=go_back, font=BUTTON_FONT, width=20).pack(pady=(20,0))

    window.mainloop()
    
                