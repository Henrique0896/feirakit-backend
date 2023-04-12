from src.program.database import database
from bson import  ObjectId
from src.service.common import Common
from src.models.enums import units_enum, categories_enum

collection = 'product'

class Product(Common):
    def get(self):
        products = list(database.main[collection].find())
        return self.entity_response_list(products)
        
    def post(self, product):
        database.main[collection].insert_one(product)
        return self.entity_response(product)

    def put(self, product):
        my_query = { '_id':  ObjectId(product['id']) }
        del product['id']
        new_values = { '$set': product}
        return database.main[collection].update_one(my_query, new_values) 

    def delete(self, id):
        database.main[collection].delete_one({'_id':  ObjectId(id)})
    
    def get_one(self, id):
        product = database.main[collection].find_one({'_id':  ObjectId(id)})
        return self.entity_response(product)

    def get_products_by_name(self, name):
        products = list(database.main[collection].find({'name_product':{'$regex': name}}))
        return self.entity_response_list(products)

    def get_products_by_id_user(self, id_user):
        products = list(database.main[collection].find({'productor_id': id_user}))
        return self.entity_response_list(products)

    def get_products_by_category(self, category):
        products = list(database.main[collection].find({"category":{'$regex': categories}}))
        return self.entity_response_list(products)

    def get_product_types(self):
        return {'units': units_enum,
                'categories': categories_enum
        }

product_service = Product()