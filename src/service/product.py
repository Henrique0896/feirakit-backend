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

    def delete(self, id):
        database.main[collection].delete_one({"_id":  ObjectId(id)})

product_service = Product()