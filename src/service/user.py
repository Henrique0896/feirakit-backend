from src.server.database import database
from bson import  ObjectId
from src.service.common import Common

collection = 'user'

class User(Common):
    def get(self):
        users = list(database.main[collection].find())
        return self.entity_response_list(users)
        
    def post(self, user):
        database.main[collection].insert_one(user)
        return self.entity_response(user)
    
    def put(self, user):
        my_query = { "_id":  ObjectId(user['id']) }
        del user["id"]
        new_values = { "$set": user}
        return database.main[collection].update_one(my_query, new_values) 

user_service = User()