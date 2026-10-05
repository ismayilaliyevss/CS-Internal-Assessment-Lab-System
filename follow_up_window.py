import tkinter as tk
from follow_up import build_follow_up_list

LABEL_FONT = ("Arial", 13)
BUTTON_FONT = ("Arial", 12)
LIST_FONT = ("Arial", 12)

def describe_days(days_left):
    if days_left < 0:
        days = -days_left 
        return f"{days} day{'s' if days != 1 else ''} overdue"
    
    if days_left == 0:
        return "due today"
    
    return f"due in {days_left} day{'s' if days_left != 1 else ''}"        # just checking whether we need to add s to the end of day word

def open_follow_up_window(staff, hash_table, back_to_menu):
    window = tk.Tk()
    window.title("Hashlab - Follow-Up Schedule")
    window.geometry("620x560")

    tk.Label(window, text=f"Logged in as: {staff.username} ({staff.staff_id}) - {staff.role}", font=LABEL_FONT).pack(pady=(15, 5))
    tk.Label(window, text= "Follow-UP Schedule", font=("Arial", 15, "bold")).pack(pady=(5, 10))

    follow_up_listbox = tk.Listbox(window, font=LIST_FONT, width=62, height=15)
    follow_up_listbox.pack()

    def refresh_list():
        follow_up_listbox.delete(0, tk.END)         # emptying the box so no duplication happens
        rows = build_follow_up_list(hash_table)     # sorting - most overdue first 

        if len(rows) == 0:
            follow_up_listbox.insert(tk.END, "No follow-ups yet - no tests have been entered")
            return

        for index, (patient, test_type, days_left) in enumerate(rows):      # what actually enumerate is giving the index (row number) together with each row
            line = f"{patient.name} {patient.surname[0]}. ({patient.phone}) - {test_type} - {describe_days(days_left)}"       # we will just give surname's only first letter
            follow_up_listbox.insert(tk.END, line)
            if days_left < 0:
                follow_up_listbox.itemconfig(index, fg="red")           # overdue rows will be in red - in real life it is mostly like this 


    def go_back():
        window.destroy()
        back_to_menu(staff)

    tk.Button(window, text="Refresh", command=refresh_list, font=BUTTON_FONT, width=20).pack(pady=(15, 0))
    tk.Button(window, text="Back to Menu", command=go_back, font=BUTTON_FONT, width=20).pack(pady=(10,0))

    refresh_list()
    window.mainloop()
