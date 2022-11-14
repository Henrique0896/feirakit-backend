from src.server.database import database
from bson import  ObjectId
from src.service.common import Common

collection = 'product'

class Product(Common):
    def get(self):
        products = list(database.main[collection].find())
        return self.entity_response_list(products)
        
    def post(self, product):
        database.main[collection].insert_one(product)
        return product

    def put(self, product):
        my_query = { "_id":  ObjectId(product['id']) }
        del product["id"]
        new_values = { "$set": product}
        return database.main[collection].update_one(my_query, new_values) 

    def delete(self, id):
        database.main[collection].delete_one({"_id":  ObjectId(id)})
    
    def get_one(self, id):
        product = database.main[collection].find_one({"_id":  ObjectId(id)})
        return self.entity_response(product)

    def get_products_by_name(self, name):
        products = list(database.main[collection].find({"nome": name}))
        return self.entity_response_list(products)

product_service = Product()