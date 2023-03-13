from pymongo import MongoClient


class Database():
    def __init__(self):
        self.client = MongoClient('DATABASE')
        self.main = self.client['feirakit-database']
        
database = Database()
