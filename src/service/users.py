from src.program.database import database
from bson import  ObjectId
from src.service.common import Common
from werkzeug.security import generate_password_hash, check_password_hash

collection = 'user'

class User(Common):
    def get(self):
        users = list(database.main[collection].find())
        if not users:
            return {'result': None,
                'message': 'Erro ao buscar usuários'}
        
        return {'result': self.entity_response_list(users),
                'message': 'Usuários retornados com sucesso'
                }

    def post(self, user):
        if(database.main[collection].find_one({"email": user['email']}) != None):
            return {'result': False,
                    'message': 'Erro ao criar usuário. Já existe um usuário com esse email'}
        user['password'] = generate_password_hash(user['password'])
        database.main[collection].insert_one(user)
        
        return {'result': True,
                'message': 'Usuário criado com sucesso'}
                    
    def put(self, user):
        old_user = database.main[collection].find_one({'_id':  ObjectId(user['id'])})
        if not old_user:
            
            return {'result': False,
                'message': 'Usuário não encontrado'
                }
        updated_user = old_user
        updated_user['name'] = user['name']
        updated_user['phone_number'] = user['phone_number']
        updated_user['adress'] = user['adress']
        my_query = { '_id':  ObjectId(user['id']) }
        new_values = { '$set': updated_user}
        database.main[collection].update_one(my_query, new_values),
        
        return {'result': self.entity_response(updated_user),    
        'message': 'Usuários retornados com sucesso'}
                

    def delete(self, id):
        user = database.main[collection].find_one({'_id':  ObjectId(id)})
        if not user:
            
            return {
                'result': False,
                'message': 'Usuário não encontrado'
                }
        database.main[collection].delete_one({'_id':  ObjectId(id)})
        
        return {
            'result': self.entity_response_list(users),
                'message': 'Usuários apagado com sucesso'
                }

    def get_one(self, id):
        user = database.main[collection].find_one({'_id':  ObjectId(id)})
        if not user:
            
            return {'result': False,
                'message': 'Usuário não encontrado'
                }
        
        return {'result': self.entity_response(user),
                'message': 'Usuário retornados com sucesso'
                }

    def get_users_by_name(self, name):
        users = list(database.main[collection].find({'name': name}))
        if not users:
            
            return {'result': False,
                'message': 'Usuário não encontrado'
                }
        
        return self.entity_response_list(users)
    
    def verify_password(self, email, password):
        user = database.main[collection].find_one({'email':  email})
        if not user:
            
            return {'result': False,
                    'message': 'Email não cadastrado'}
        if not check_password_hash(user['password'], password):
            return {'result': False,
                    'message': 'Senha inválida'}
        
        return {'result': True,
                'message': 'Senha verificada'}
    
    def change_password(self, email, old_password, new_password):
        valid_old_password = self.verify_password(email, old_password)
        if valid_old_password['result']:
            user = database.main[collection].find_one({'email':  email})
            user['password'] = generate_password_hash(new_password)
            my_query = { 'email':  email }
            new_values = { '$set': user}
            database.main[collection].update_one(my_query, new_values)
            
            return {'result': True,
                    'message': 'Senha alterada com sucesso'}
        if valid_old_password['message'] == 'Senha inválida':
            
            return {'result': False,
                    'message': 'Senha antiga é inválida'}

        return valid_old_password
    
    def get_users_by_email(self, email):
        users = list(database.main[collection].find({"email": email}))
        if not users:
            
            return {'result': None,
                    'message': 'Não foi possível buscar usuários'}
        
        return {'result': self.entity_response_list(users),
                'message': 'Usuários retornados com sucesso'}
        
    
user_service = User()
