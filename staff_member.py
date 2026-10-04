import hashlib 
from db import get_staff_by_username

def hash_password(password):
    # here we will use python's built in hashlib - turns the password into a fixed length one-way hash (cannot be reversed)
    return hashlib.sha256(password.encode()).hexdigest()    # because of sha256 the password is one-way, and also same input always gives the exact same output

class StaffMember:
    def __init__(self, staff_id, username, password_hash, role):
        self.staff_id = staff_id
        self.username = username
        self.password_hash = password_hash                  # the password is already hashed - does not store the real password
        self.role = role

def login(username, password):
    row = get_staff_by_username(username)                   # gives us the whole row of the data of the staff member - finds from the username

    if row is None:                                         # checking if the given username is sufficient or not
        return "Error: incorrect username or password"
    else:
        login_password = hash_password(password)            # if the username exists in the database, hashes the password

    staff_id, db_username, stored_hash, role = row          # putting row's data into different variables

    if login_password != stored_hash:                       # checking if the freshly hashed password matches the stored hashed password in the database
        return "Error: incorrect username or password"
    
    return StaffMember(staff_id, db_username, stored_hash, role)    # if it matches the stored hashed password, creates StaffMember object
    