from pymongo import MongoClient
from src.core.settings_env import settings_env
class Database():
    def __init__(self):
        self.client = MongoClient(settings_env.get_var("DB_CONNECTION"))
        self.main = self.client[settings_env.get_var("DATABASE")]

database = Database()
