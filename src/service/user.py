from src.server.database import database
from bson import  ObjectId
from src.service.common import Common

collection = 'user'

class User(Common):
    async def get(self):
        users = await list(database.main[collection].find())
        return self.entity_response_list(users)
        
    async def post(self, user):
        await database.main[collection].insert_one(user)
        return self.entity_response(user)
    
    async def put(self, user):
        my_query = { "_id":  ObjectId(user['id']) }
        del user["id"]
        new_values = { "$set": user}
        return await database.main[collection].update_one(my_query, new_values) 

    async def delete(self, id):
        await database.main[collection].delete_one({"_id":  ObjectId(id)})

    async def get_one(self, id):
        user = database.main[collection].find_one({"_id":  ObjectId(id)})
        return await self.entity_response(user)

    async def get_users_by_name(self, name):
        users = list(database.main[collection].find({"nome_completo": name}))
        return await self.entity_response_list(users)

user_service = User()