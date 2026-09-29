class HashTable:
    def __init__(self, size=100):   # number of slots in the table
        self.size = size            # make the hash funciton easier to read
        self.table = []             # starting with an empty list    
        for _ in range(size):       # repeating 100 times - 100 slots
            self.table.append([])   # each time adding one empty list to it - each slot

    def hash(self, key):            # key is the patient's phone number
        total = 0
        for char in str(key):   
            total += ord(char)      # turning each character into its code and add it
        return total % self.size    # squeeze into range 0-99

    def insert(self, patient):      # value is the actual record of the patient
        index = self.hash(patient.phone)      # finding which slot this key belongs in
        self.table[index].append(patient)     # storing whole Patient object

    def search(self, key):
        index = self.hash(key)
        for patient in self.table[index]:
            if patient.phone == key:          # patient.phone is the stored key - checking if it matches
                return patient      # patient is the whole object - if matches return it
        return None