import calendar
from datetime import date

def load_thresholds(filename = "thresholds.txt"):   # we are using the external file - as mentioned in the crtirerion C - if a clinic changes a guideline, only this thresholds.txt file needs editing - no change in coding part
    thresholds ={}
    file = open(filename, "r")
    for line in file:
        line = line.strip()                         # removes the \n at the end of the line
        if line == "":                              # I added this code to skip the blank lines - just in case
            continue
        parts = line.split("-")                     # dash-seperated - I used the same order as Image 11 (criterion C)
        test_name = parts[0]
        cutoff_value = float(parts[1])
        unit = parts[2]
        interval_months = int(parts[3])
        direction = parts[4]

        thresholds[test_name] = {                   # each test type has its own threshold and direction (I used dictionary into dictionary for saving threshold info)
            "limit": cutoff_value,
            "unit": unit, 
            "interval": interval_months,
            "direction": direction
        }
    file.close()
    return thresholds

class Test:
    def __init__(self, test_type, result_value, test_date):
        self.test_type = test_type
        self.result_value = result_value            # the actual number from the lab result
        self.test_date = test_date                  # needed for calculatinf the follow-up due date
        self.classification = None                  # not calculated yet - will be set by classify() function 
        self.next_due_date = None                   # not calculated yet - will be set by calculate_due_date() funciton

    def classify(self):
        thresholds = load_thresholds()              # read from thresholds.txt instead of directly from code - makes it easier for hospital to change the guidelines of thresholds

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
        thresholds = load_thresholds()               # interval_months lives in the thresholds.txt file 
        months_to_add = thresholds[self.test_type]["interval"]

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