from patient import Patient
from datetime import date
import sqlite3
from db import save_patient

def generate_patient_id():
    conn = sqlite3.connect("hashlab.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM patients")     # so everytime when code runs, it will continue to generate the ID from the leftover ID. For ex, code stopped after creating P003, when it runs again it will continue to generate from  P004
    count = cursor.fetchone()[0]
    conn.close()
    return "P" + str(count + 1).zfill(3)                # For example, P001

def register_patient(name, surname, phone, hash_table):
    if not name or not surname or not phone:
        return "Error: all fields are required"         # checking if all fields filled

    if not phone.isdigit() or len(phone) != 10:
        return "Error: invalid phone number format"     # checking if phone format is valid? (should be 10 digit)

    existing = hash_table.search(phone)                 # checking if already exists? - using search() from hash_table.py 
    if existing is not None:
        return "Error: patient already registered"

    new_id = generate_patient_id()
    new_patient = Patient(new_id, name, surname, phone, date.today())  # create and store the new patient, records today's date as registration date - for report generation
    hash_table.insert(new_patient)
    save_patient(new_patient)
    return new_patient
