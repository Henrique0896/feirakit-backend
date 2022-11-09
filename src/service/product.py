from src.server.database import database
from bson import json_util, ObjectId
import json

collection = 'product'

class Product():
    def get(self):
        list_data_products =  list(database.main[collection].find())
        products = []
        for data_product in list_data_products:
            product = json.loads(json_util.dumps(data_product))
            product['id'] = product['_id']['$oid']
            products.append(product)
        return products
        
    def post(self, product):
        database.main[collection].insert_one(product)
        return product

    def put(self, product):
        myquery = { "_id":  ObjectId(product['id']) }
        newvalues = { "$set": product}
        return database.main[collection].update_one(myquery, newvalues) 

    def delete(self, id):
        database.main[collection].delete_one({"_id":  ObjectId(id)})
    
    def get_one(self, id):
        return database.main[collection].find_one({"_id":  ObjectId(id)})
    

product_service = Product()