from pymongo import MongoClient
import os

class Database():
    def __init__(self):
        self.client = MongoClient(os.environ['DATABASE'])
        self.main = self.client['feirakit-database']
        
database = Database()
