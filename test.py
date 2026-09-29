import calendar
from datetime import date
class Test:
    def __init__(self, test_type, result_value, test_date):
        self.test_type = test_type
        self.result_value = result_value            # the actual number from the lab result
        self.test_date = test_date                  # needed for calculatinf the follow-up due date
        self.classification = None                  # not calculated yet - will be set by classify() function 
        self.next_due_date = None                   # not calculated yet - will be set by calculate_due_date() funciton

    def classify(self):
        thresholds = {          # each test type has its own threshold and direction (I used dictionary into dictionary for saving threshold info)
            "HbA1c":        {"limit": 6.5, "direction": "above"},   # "above" = positive if result is high
            "Lipid":  {"limit": 200, "direction": "above"},
            "CBC":          {"limit": 13.0, "direction": "below"}   # "below" = positive if result is low
        }

        info = thresholds[self.test_type]

        if info["direction"] == "above":
            if self.result_value > info["limit"]:
                self.classification = "positive"
            else:
                self.classification = "negative"
        else:
            if self.result_value < info["limit"]:
                self.classification = "positive"
            else:
                self.classification = "negative"

    def calculate_due_date(self):
        intervals = {"HbA1c": 3, "Lipid":6, "CBC": 12}        #using dictionary again for interval info
        months_to_add = intervals[self.test_type]

        year = self.test_date.year
        month = self.test_date.month + months_to_add
        day = self.test_date.day

        while month > 12:           #rolling over the next year if needed
            month -= 12
            year += 1

        #calendar.monthrange(year, month) returns weekday of 1st and number of days in that month
        last_day_of_month = calendar.monthrange(year, month) [1]        # but I only need second value - how many days this month has 
        day = min(day, last_day_of_month)       # for example, if 31 does not exist - use the last real day

        self.next_due_date = date(year, month, day)