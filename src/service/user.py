from src.program.database import database
from bson import  ObjectId
from src.service.common import Common
from werkzeug.security import generate_password_hash, check_password_hash

collection = 'user'

class User(Common):
    def get(self):
        users = list(database.main[collection].find())
        return self.entity_response_list(users)
        
    def post(self, user):
        user['senha'] = generate_password_hash(user['senha'])
        database.main[collection].insert_one(user)
        return self.entity_response(user)
    
    def put(self, user):
        old_user = database.main[collection].find_one({'_id':  ObjectId(user['id'])})
        if not old_user:
            return "Erro ao atualizar usuário. Não foi possível encontrar um usuário pelo id: {}.".format(user['id'])
        updated_user = old_user
        updated_user['nome'] = user['nome']
        updated_user['telefone'] = user['telefone']
        updated_user['endereco'] = user['endereco']
        my_query = { '_id':  ObjectId(user['id']) }
        new_values = { '$set': updated_user}
        return database.main[collection].update_one(my_query, new_values) 

    def delete(self, id):
        user = database.main[collection].find_one({'_id':  ObjectId(id)})
        if not user:
            return "Erro ao apagar usuário. Não foi possível encontrar um usuário pelo id: {}.".format(user['id'])
        database.main[collection].delete_one({'_id':  ObjectId(id)})

    def get_one(self, id):
        user = database.main[collection].find_one({'_id':  ObjectId(id)})
        return self.entity_response(user)

    def get_users_by_name(self, name):
        users = list(database.main[collection].find({'nome': name}))
        return self.entity_response_list(users)
    
    def verify_password(self, email, password):
        user = database.main[collection].find_one({'email':  email})
        if not user:
            return {'resultado': False,
                    'mensagem': 'Email não cadastrado'}
        if not check_password_hash(user['senha'], password):
            return {'resultado': False,
                    'mensagem': 'Senha inválida'}
        return {'resultado': True,
                'mensagem': 'Senha verificada'}
    
    def change_password(self, email, old_password, new_password):
        valid_old_password = self.verify_password(email, old_password)
        if valid_old_password['resultado']:
            user = database.main[collection].find_one({'email':  email})
            user['senha'] = generate_password_hash(new_password)
            my_query = { 'email':  email }
            new_values = { '$set': user}
            database.main[collection].update_one(my_query, new_values)
            return {'resultado': True,
                    'mensagem': 'Senha alterada com sucesso'}
        if valid_old_password['mensagem'] == 'Senha inválida':
            return {'resultado': False,
                    'mensagem': 'Senha antiga é inválida'}
        return valid_old_password
        



user_service = User()