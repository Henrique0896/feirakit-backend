from src.server.database import database
from bson import  ObjectId
from src.service.common import Common

collection = 'kit'

class Kit(Common):
    def get(self):
        kits = list(database.main[collection].find())
        return self.entity_response_list(kits)

    def post(self, kit):
        database.main[collection].insert_one(kit)
        return self.entity_response(kit)


    def delete(self, id):
        database.main[collection].delete_one({"_id":  ObjectId(id)})
    
    def put(self, kit):
        my_query = { "_id":  ObjectId(kit['id']) }
        del kit["id"]
        new_values = { "$set": kit}
        return database.main[collection].update_one(my_query, new_values) 

kit_service = Kit()