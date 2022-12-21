from src.server.database import database
from bson import  ObjectId
from src.service.common import Common

collection = 'receita'

class Receita(Common):
    def get(self):
        receitas = list(database.main[collection].find())
        return self.entity_response_list(receitas)
        
    def post(self, receita):
        database.main[collection].insert_one(receita)
        return self.entity_response(receita)

    def put(self, receita):
        my_query = { "_id":  ObjectId(receita['id']) }
        del receita["id"]
        new_values = { "$set": receita}
        return database.main[collection].update_one(my_query, new_values) 

    def delete(self, id):
        database.main[collection].delete_one({"_id":  ObjectId(id)})
    
    
receita_service = Receita()