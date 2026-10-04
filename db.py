import sqlite3
from datetime import date
from hash_table import HashTable
from patient import Patient
from test import Test

def create_tables():
    conn = sqlite3.connect("hashlab.db")     # opens/creates a file called hashlab.db - this file is the database on the computer - conn opens connection to the database
    cursor = conn.cursor()                   # cursor is for writing/reading inside the database - conn itself cannot run SQL commands - so we use cursor

    # execute - runs one SQL command through that connection - the command is CREATE TABLE in our case
    cursor.execute( """                      
        CREATE TABLE IF NOT EXISTS patients (                     
            patient_id TEXT PRIMARY KEY, 
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            visit_count INTEGER NOT NULL DEFAULT 0,
            registered_date TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tests (                       
            test_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id TEXT NOT NULL,
            test_type TEXT NOT NULL,
            result REAL NOT NULL,
            classification TEXT,
            test_date TEXT NOT NULL,
            next_due_date TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    """)

    conn.commit()       # saves the changes permanently to hashlab.db
    conn.close()        # closes the connection

def save_patient(patient):      # saving the data of patient - inserting one new row into patients table
    conn = sqlite3.connect("hashlab.db")
    cursor = conn.cursor()

    # we include patient_id - because it is string and SQLite cannot AUTOINCREMENT strings, so we generate the patient_id by funtction - generate_patient_id() in registration.py

    cursor.execute(
        "INSERT INTO patients (patient_id, name, surname, phone, visit_count, registered_date) VALUES (?,?,?,?,?,?)",
        (patient.patient_id, patient.name, patient.surname, patient.phone, patient.visit_count, patient.registered_date)
    )
    conn.commit()
    conn.close()

def save_test(test, patient_id):    # saving the data about test - inserting one new row into tests table
    conn = sqlite3.connect("hashlab.db")
    cursor = conn.cursor()

    # we do not include test_id here - because it is integer so we can just AUTOINCREMENT - SQLite will assign the number automatically

    cursor.execute(
        "INSERT INTO tests (patient_id, test_type, result, classification, test_date, next_due_date) VALUES (?,?,?,?,?,?)",
        (patient_id, test.test_type, test.result_value, test.classification, test.test_date, test.next_due_date)
    )
    conn.commit()
    conn.close()

def update_patient(patient):    # updates an existing patient's saved data - save_patient() - only INSERT new rows, so after visit_count changes - this function would write the change back to the database 
    conn = sqlite3.connect("hashlab.db")
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE patients SET visit_count = ? WHERE patient_id = ?",
        (patient.visit_count, patient.patient_id)
    )
    conn.commit()
    conn.close()

def load_all_patients():        # most IMPORTANT part of our SQlite coding - this function takes all the data from the database and reload it to the OOP - because OOP in RAM does not hold the data after shutting down the system - so we need to reload the data from database to the objects to be able to edit the data
    conn = sqlite3.connect("hashlab.db")
    cursor = conn.cursor()

    hash_table = HashTable()    # starting with an empty and new hash table to rebuild into
    patients_by_id = {}         # temporary lookup just for linking tests to patients during loading stage

    # first step - loading every patient row and recreate Patient objects
    cursor.execute("SELECT patient_id, name, surname, phone, visit_count, registered_date FROM patients")       # getting the data from database table columns - patients
    patient_rows = cursor.fetchall()        # this returns a list of tuples - one tuple per row

    for row in patient_rows:                # unpacking the tuple into variables - in the same order as the SELECT columns
        patient_id, name, surname, phone, visit_count, registered_date_str = row

        registered_date = date.fromisoformat(registered_date_str)       # as dates are stored as TEXT in SQLite - we need to convert it to real date object

        patient = Patient(patient_id, name, surname, phone, registered_date)
        patient.visit_count = visit_count                               # overwrites the default 0 with the saved value in database

        hash_table.insert(patient)                                      # putting the rebuilted patient back into the hash table
        patients_by_id[patient_id] = patient                            # remembering it by ID too, just for this function

    # second step - load every test row and attach it to the patient it belongs to 
    cursor.execute("SELECT patient_id, test_type, result, classification, test_date, next_due_date FROM tests")   # getting the data from database table columns - tests
    test_rows = cursor.fetchall()

    for row in test_rows:
        patient_id, test_type, result, classification, test_date_str, next_due_date_str = row
        patient = patients_by_id[patient_id]                            # looked up by ID here - as we used dictionary its time complexity is only O(1)       

        test = Test(test_type, result, date.fromisoformat(test_date_str))
        test.classification = classification                            # classify() already ran before saving - so just restoring the result
        test.next_due_date = date.fromisoformat(next_due_date_str)      # same for the due date - I explained it above

        patient.add_test(test)

    conn.close()
    return hash_table