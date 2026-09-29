from test import Test

def enter_test_result(phone, test_type, result_value, test_date, hash_table):
    patient = hash_table.search(phone)              #finding the patient first, reusing search()
    if patient is None:
        return "Error: patient not found"

    new_test = Test(test_type, result_value, test_date)     # creating the Test object and using its two methods
    new_test.classify()                                     # first method - classify()
    new_test.calculate_due_date()                           # second method - calculate_due_date()

    patient.add_test(new_test)                              # attaching it to the patient

    same_day_test_exists = False                            # only count a new visit if no earlier test already happened on this same date
    for existing_test in patient.tests[:-1]:                # excluding the test we just added
        if existing_test.test_date == test_date:
            same_day_test_exists = True
            break

    if not same_day_test_exists:
        patient.register_visit()                            # only increasing visit count if it is the first test of that date

    return new_test
    