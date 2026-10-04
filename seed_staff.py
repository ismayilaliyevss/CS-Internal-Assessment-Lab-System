import random
from db import create_tables, save_staff
from staff_member import StaffMember, hash_password

create_tables()         # making sure that staff table exists before we insert into it

numbers = random.sample(range(1000, 10000), 40)     # picks 40 random numbers between 1000 and 10000 - and when it selects one number, it is removed from what is left to choose from - this prevents creating same passwords

credentials = []            #  whole data about a staff member will go to here - staff_id, username, password, role - so we will have a file to see the passwords and usernames
staff_id_counter = 1     
number_index = 0

for i in range(1, 6):
    username = f"tech{i}"   # building the username , for example: tech1, tech2
    password = f"hashlab{numbers[number_index]}"    # builds the password by grabbing numbers[number_index]
    number_index += 1
    staff_id = f"S{staff_id_counter:03d}"           # for example, S001
    save_staff(StaffMember(staff_id, username, hash_password(password), "Technician"))      # saving all the data to the StaffMember object
    credentials.append((staff_id, username, password, "Technician"))        # puts everything to the credentials, so me as an IT manager can check every data about the staff - and also saves the password without hashing
    staff_id_counter += 1

for i in range(1, 36):
    username = f"doc{i}"
    password = f"hashlab{numbers[number_index]}"
    number_index += 1
    staff_id = f"S{staff_id_counter:03d}"
    save_staff(StaffMember(staff_id, username, hash_password(password), "Doctor"))
    credentials.append((staff_id, username, password, "Doctor"))
    staff_id_counter += 1

with open("seeded_credentials.txt", "w") as f:              # this helps us to put credentials to the new text file seeded_credentials.txt
    f.write("staff_id\tusername\tpassword\trole\n")
    for staff_id, username, password, role in credentials:
        f.write(f"{staff_id}\t{username}\t{password}\t{role}\n")
 
print(f"Created {len(credentials)} staff accounts.")          # just to check if this file works correctly
