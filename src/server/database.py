from pymongo import MongoClient

class Database():
    def __init__(self):
        self.client = MongoClient('DB_CONNECTION')
        self.main = self.client['DATABASE']

database = Database()