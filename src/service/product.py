from src.program.database import database
from bson import  ObjectId
from src.service.common import Common
from src.models.enums import unidade_enum, categoria_enum

collection = 'product'

class Product(Common):
    def get(self,page,limit,sort):
        skip = limit * (page - 1)
        products = list(database.main[collection].find().skip(skip).limit(limit).sort('_id',sort))
        return self.entity_response_list(products)
        
    def post(self, product):
        database.main[collection].insert_one(product)
        return self.entity_response(product)

    def put(self, product,current_user):
        print(product['produtor_id'])
        if product['produtor_id'] != current_user['id']:
             return {
                    'resultado': False,
                    'mensagem': "erro ao atualizar produto,esse produto pertence a outro usuário"
                  },403

        my_query = { '_id':  ObjectId(product['id']) }
        del product['id']
        new_values = { '$set': product}
        return database.main[collection].update_one(my_query, new_values) 

    def delete(self, id,current_user): 
        product=database.main[collection].find_one({'_id':  ObjectId(id)})
        if product['produtor_id'] != current_user['id']:
           return {
                    'resultado': False,
                    'mensagem': "erro ao apagar produto,esse produto pertence a outro usuário"
                  },403
        database.main[collection].delete_one({'_id':  ObjectId(id)})
        return {
                    'resultado': True,
                    'mensagem': "Produto apagado com sucesso"
                  }
    
    def get_one(self, id):
        product = database.main[collection].find_one({'_id':  ObjectId(id)})
        return self.entity_response(product)
    
    def get_products_by_name(self, name):
        products = list(database.main[collection].find({'nome':{'$regex': name}}))
        return self.entity_response_list(products)

    def get_products_by_id_usuario(self, id_usuario):
        products = list(database.main[collection].find({'produtor_id': id_usuario}))
        return self.entity_response_list(products)
    
    def get_product_types(self):
        return {
                    'unidades': unidade_enum,
                    'categorias': categoria_enum
                }

product_service = Product()