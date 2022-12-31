from pymongo import MongoClient

class Database():
    def __init__(self):
        self.client = MongoClient('mongodb+srv://valeadmin:7dpf7pfqvOt9IDsq@vale01.r9ngupt.mongodb.net/?retryWrites=true&w=majority')
        self.main = self.client['feirakit-database']

database = Database()