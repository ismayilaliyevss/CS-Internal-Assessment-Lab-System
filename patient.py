class Patient:
    def __init__(self, patient_id, name, surname, phone, registered_date):
        self.patient_id = patient_id
        self.name = name
        self.surname = surname
        self.phone = phone
        self.registered_date = registered_date      #needed for report generation which patients registered in a given period
        self.visit_count = 0        # starts at 0 - no visits yet
        self.tests = []             # empty list - no test history yet

    def add_test(self, test):
        self.tests.append(test)
        
    def register_visit(self):
        self.visit_count += 1       # each new test/visit increases visit count

    def get_discount(self):
        if self.visit_count >= 5:
            return 0.10             # 10% after 5 visits
        elif self.visit_count >= 3:
            return 0.05             # 5% after 3 visits
        else: 
            return 0.0              # no discount yet