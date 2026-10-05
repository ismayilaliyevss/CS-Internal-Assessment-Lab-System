import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta
from report import generate_report

LABEL_FONT = ("Arial", 13)
BUTTON_FONT = ("Arial", 12)
ENTRY_FONT = ("Arial", 13)

PERIODS = ["Weekly", "Monthly", "Yearly"]           # so users can select between these period options
TEST_TYPES = ["HbA1c", "Lipid", "CBC"]       

def get_period_dates(period):               # this function is basically turns period choice to start date and end date
    today = date.today()
    if period == "Weekly":
        start= today - timedelta(days=6)    # counting today also, last 7 days
    elif period == "Monthly":
        start = today.replace(day=1)        # 1st of the current month
    else:
        start = today.replace(month=1, day=1)   # 1 january of the current year
    return start, today

def open_report_window(staff, hash_table, back_to_menu):
    window = tk.Tk()
    window.title("HashLab - Generate Report")
    window.geometry("480x560")

    tk.Label(window, text=f"Logged in as: {staff.username} ({staff.staff_id}) - {staff.role}", font=LABEL_FONT).pack(pady=(15, 5))
    tk.Label(window, text="Generate Report", font=("Arial", 15, "bold")).pack(pady=(5, 10))

    period_box = ttk.Combobox(window, values = PERIODS, state="readonly", font=ENTRY_FONT, width=14)
    period_box.current(1)           # I just chose to start with Monthly - as it is the most used one
    period_box.pack()

    result_frame = tk.Frame(window, relief="solid", bd=1)       # it is basically a box inside the window - this box will hold the summary

    period_label = tk.Label(result_frame, text="Period: -", font=LABEL_FONT, anchor="w")
    registration_label = tk.Label(result_frame, text="Total registrations: -", font=LABEL_FONT, anchor="w")
    test_labels = {}

    for test_type in TEST_TYPES:
        test_labels[test_type] = tk.Label(result_frame, text=f"{test_type} - -", font=LABEL_FONT, anchor="w")

    discounts_label = tk.Label(result_frame, text="Total discounts applied: -", font=LABEL_FONT, anchor="w")

    def generate():
        start, end = get_period_dates(period_box.get())
        total_registration, positive_counts, negative_counts, total_discounts = generate_report(start, end, hash_table)     # same order from the report.py

        period_label.config(text=f"Period: {start.strftime('%d/%m/%Y')} - {end.strftime('%d/%m/%Y')}")
        registration_label.config(text=f"Total registrations: {total_registration}")
        for test_type in TEST_TYPES:
            positives = positive_counts.get(test_type, 0)       # 0 is for when there is no any positive
            negatives = negative_counts.get(test_type, 0)
            test_labels[test_type].config(text=f"{test_type} - {positives} positive / {negatives} negative")

        discounts_label.config(text=f"Total discounts applied: {total_discounts}")

    def go_back():
        window.destroy()
        back_to_menu(staff)

    tk.Button(window, text="Generate", command=generate, font=BUTTON_FONT, width=20).pack(pady=10)

    result_frame.pack(padx=20, pady=10, fill="x")
    period_label.pack(fill="x", padx=10, pady=(10, 4))      # fill x basically means that widget can stretch as much as the size of whatever it is inside
    registration_label.pack(fill="x", padx=10, pady=4)
    for test_type in TEST_TYPES:
        test_labels[test_type].pack(fill="x", padx=10, pady=4)
    discounts_label.pack(fill="x", padx=10, pady=(4, 10))

    tk.Button(window, text="Back to Menu", command=go_back, font=BUTTON_FONT, width=20).pack(pady=(10, 0))

    window.mainloop()
