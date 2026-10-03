def generate_report(start_date, end_date, hash_table):
    total_registration = 0
    positive_counts = {"HbA1c" : 0, "Lipid" : 0, "CBC" : 0}         # one counter per test type
    negative_counts = {"HbA1c" : 0, "Lipid" : 0, "CBC" : 0}         
    total_discounts = 0

    for patient in hash_table.get_all_patients():
        if start_date <= patient.registered_date and patient.registered_date <= end_date:       # checking whether if this patient registered in the chosen period
            total_registration += 1

        for test in patient.tests:
            if start_date <= test.test_date and test.test_date <= end_date:
                if test.classification == "positive":
                    positive_counts[test.test_type] += 1
                else:
                    negative_counts[test.test_type] += 1
                # I feel this part is really important to understand - so it checks how many visits had this patient had AS OF this test's own date
                visits_so_far = count_visits_up_to(patient, test.test_date)
                if get_discount_for_visit_count(visits_so_far) > 0:
                    total_discounts += 1

    return total_registration, positive_counts, negative_counts, total_discounts

def count_visits_up_to(patient, as_of_date):
    distinct_dates = set()          # a visit is one distinct date. so we collect every test date up to as_of_date - then put it to a set - then count this set
    for test in patient.tests:
        if test.test_date <= as_of_date:
            distinct_dates.add(test.test_date)

    return len(distinct_dates)

def get_discount_for_visit_count(visit_count):
    if visit_count >= 5:
        return 0.10
    elif visit_count >=3:
        return 0.05
    else:
        return 0.0