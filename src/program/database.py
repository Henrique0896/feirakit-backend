from pymongo import MongoClient
import os
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())


class Database():
    def __init__(self):
        self.client = MongoClient(os.getenv("DB_CONNECTION"))
        self.main = self.client[os.getenv("DATABASE")]


database = Database()
