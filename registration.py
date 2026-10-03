from patient import Patient
from datetime import date
next_patient_id = 1         # module-level counter, resets to 1 on every start so will be replaced by SQLite later

def generate_patient_id():
    global next_patient_id
    new_id = "P" + str(next_patient_id).zfill(3)        # for example, 1-> "P001"
    next_patient_id += 1
    return new_id

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
    return new_patient
