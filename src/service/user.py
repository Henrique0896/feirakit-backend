from bson import  ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from jwt import encode
from src.service.id_settings import IdSettings
from src.program.database import database
from src.core.settings_env import settings_env

class User(IdSettings):
    def __init__(self):
        self.collection = 'user'

    def get(self):
        users = list(database.main[self.collection].find())
        if not users:
            return {'resultado': None,
                'mensagem': 'Erro ao buscar usuários'}
        return {'resultado': self.entity_response_list(users),
                'mensagem': 'Usuários retornados com sucesso'}

    def post(self, user):
        if(database.main[self.collection].find_one({"email": user['email']}) != None):
            return {'resultado': False,
                    'mensagem': 'Erro ao criar usuário. Já existe um usuário com esse email'},209
        user['senha'] = generate_password_hash(user['senha'])
        database.main[self.collection].insert_one(user)
        return {'resultado': True,
                'mensagem': 'Usuário criado com sucesso'},201
                    
    def put(self, user,current_user):
        old_user = database.main[self.collection].find_one({'_id':  ObjectId(user['id'])})
        
        if not old_user:
            return {'resultado': {},
                    'mensagem': 'Erro ao atualizar usuário. Usuário não encontrado'},404
        
        if str(old_user['_id'])!=current_user['id']:
            return {'resultado': {},
                    'mensagem': 'Erro ao atualizar usuário. Você não tem permissão para alterar este usuário'},403

        updated_user = old_user
        updated_user['nome'] = user['nome']
        updated_user['telefone'] = user['telefone']
        updated_user['endereco'] = user['endereco']
        my_query = { '_id':  ObjectId(user['id']) }
        new_values = { '$set': updated_user}
        database.main[self.collection].update_one(my_query, new_values)
        return {'resultado': self.entity_response(updated_user),
                'mensagem': 'Usuário alterado com sucesso'},201
         

    def delete(self, id,current_user):
        user = database.main[self.collection].find_one({'_id':  ObjectId(id)})
        if not user:
            return {
            "resultado": False,
            "mensagem": "Erro ao apagar usuário. Não foi possível encontrar este usuário"
            },404
        
        if str(user['_id'])!=current_user['id']:
            return {
            "resultado": False,
            "mensagem": "Erro ao apagar usuário. Estas informações pertencem à outro usuário"
            },401
       
        database.main[self.collection].delete_one({'_id':  ObjectId(id)})

        return {
            "resultado": True,
            "mensagem": "usuário deletado com sucesso"
            },204

    def get_one(self, id):
        user = database.main[self.collection].find_one({'_id':  ObjectId(id)})
        return {'resultado': self.entity_response(user),
                    'mensagem': 'Usuário retornado com sucesso'}

    def get_users_by_name(self, name):
        users = list(database.main[self.collection].find({'nome': name}))
        return {'resultado': self.entity_response_list(users),
                    'mensagem': 'Usuários retornados com sucesso'}
    
    def verify_password(self, email, password):
        user = database.main[self.collection].find_one({'email':  email})
        if not user:
            return {'resultado': False,
                    'token':'null',
                    'mensagem': 'Email não cadastrado'}
        
        if not check_password_hash(user['senha'], password):
            return {'resultado': False,
                    'token':'null',
                    'mensagem': 'Senha inválida'}
        payload={
           "id":str(user['_id']),
           "nome": user['nome']
        }

        secret= settings_env("SECRET_KEY")
        token=encode(payload,secret)

        return {'resultado': True,
                'token':token,
                'mensagem': 'Senha verificada'}
    
    def change_password(self, email, old_password, new_password,current_user):
        valid_old_password = self.verify_password(email, old_password)
        if valid_old_password['resultado']:
            user = database.main[self.collection].find_one({'email':  email})
            if str(user['_id']) != current_user['id']:
                 return {'resultado': False,
                         'mensagem': 'Você não tem permissão para alterar este dado'},401

            user['senha'] = generate_password_hash(new_password)
            my_query = { 'email':  email }
            new_values = { '$set': user}
            database.main[self.collection].update_one(my_query, new_values)
            return {'resultado': True,
                    'mensagem': 'Senha alterada com sucesso'},200
        
        if valid_old_password['mensagem'] == 'Senha inválida':
            return {'resultado': False,
                    'mensagem': 'Senha antiga é inválida'},401 
        if valid_old_password['mensagem'] == 'Email não cadastrado':
            return {'resultado': False,
                    'mensagem': 'Email não cadastrado'},404
        
    
    def get_users_by_email(self, email):
        users = list(database.main[self.collection].find({"email": email}))
        if not users:
            return {'resultado': None,
                'mensagem': 'Não foi possível buscar usuários'}
        return {'resultado': self.entity_response_list(users),
                'mensagem': 'Usuários retornados com sucesso'}
        
    
user_service = User()