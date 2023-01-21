from pymongo import MongoClient

class Database():
    def __init__(self):
        self.client = MongoClient('link')
        self.main = self.client['feirakit-database']
        

database = Database()