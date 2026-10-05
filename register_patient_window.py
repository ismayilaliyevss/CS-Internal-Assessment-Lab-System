import tkinter as tk
from hash_table import HashTable
from registration import register_patient

LABEL_FONT = ("Arial", 13)          # firstly, I was writing them by hand each time, but whenever I tried to change it - it became so hard to change for each text, so I just created variables - make it easier to modify
BUTTON_FONT = ("Arial", 12)
ENTRY_FONT = ("Arial", 13)

def open_register_patient_window(staff, hash_table, back_to_menu):      # we need staff for going back to menu
    window = tk.Tk()
    window.title("HashLab - Register Patient")
    window.geometry("380x380")

    tk.Label(window, text = "Name", font = LABEL_FONT).pack(pady=(15,0))
    name_entry = tk.Entry(window, font = ENTRY_FONT)
    name_entry.pack()

    tk.Label(window, text = "Surname", font=LABEL_FONT).pack(pady=(10,0))
    surname_entry = tk.Entry(window, font = ENTRY_FONT)
    surname_entry.pack()

    tk.Label(window, text="Phone Number (10 digits)", font=LABEL_FONT).pack(pady=(10,0))        # in photo 6 I wrote it as Phone/ID - the thing I wanted to explain was that phone is our ID - we will do the hashing with phone number not anything else
    phone_entry = tk.Entry(window, font=ENTRY_FONT)
    phone_entry.pack()

    def attempt_register():
        name = name_entry.get()
        surname = surname_entry.get()
        phone = phone_entry.get()

        result = register_patient(name, surname, phone, hash_table)

        if isinstance(result, str):                 # register_patient would return the error message - string if something went wrong and returns a Patient object when it worked 
            message_label.config(text=result, fg="red")     # when it returns error string
        else:
            message_label.config(text=f"Registered {result.name} {result.surname} as {result.patient_id}", fg="green")
            name_entry.delete(0, tk.END)            # clearing the boxes - ready for next registration
            surname_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)

    tk.Button(window, text="Register", command=attempt_register, font=BUTTON_FONT, width=20).pack(pady=5)

    message_label = tk.Label(window, text="", font=LABEL_FONT, fg="red", wraplength=340)        # it is empty until register button is clicked, and so attempt_register() function called
    message_label.pack(pady=(10,0))

    def go_back():
        window.destroy()
        back_to_menu(staff)
    tk.Button(window, text="Back to Menu", command=go_back, font=BUTTON_FONT, width=20).pack(pady=(15,0))


    window.mainloop()

