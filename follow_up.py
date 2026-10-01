from datetime import date

def build_follow_up_list( hash_table, today = None):
    if today is None:
        today = date.today()            # must be calculated here not as the default value above - because default values are only set once - so it would freeze at the wrong date forever

    follow_up_list = []
    test_types = ["HbA1c", "Lipid", "CBC"]

    for patient in hash_table.get_all_patients():           # goes through every patient in the system
        for test_type in test_types:
            latest = None                                   # nothing found yet for this test_type of this patient
            for test in patient.tests:                      # going through every test this patient ever had 
                if test.test_type == test_type:             
                    if latest is None or test.test_date > latest.test_date:         # checks if this is the first test checked or newer than the old one 
                        latest = test                                               # if yes, remembers it as the newest one found so far 

            if latest is not None:                          # patient had this test type before
                days_left = (latest.next_due_date - today).days
                follow_up_list.append((patient, test_type, days_left))              # adds the necessary 3 info to the follow_up_list


    follow_up_list.sort(key = lambda entry: entry[2])       # most overdue - most negative first
    return follow_up_list