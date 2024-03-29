from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from jwt import encode
from src.service.id_settings import IdSettings
from src.program.database import database
from src.core.var_env import var_env
import secrets
import smtplib


class User(IdSettings):
    def __init__(self):
        self.collection = 'user'

    def get(self):
        users = list(database.main[self.collection].find())
        if not users:
            return {'resultado': None,
                    'mensagem': 'Erro ao buscar usuários'}, 404
        return {'resultado': self.entity_response_list(users),
                'mensagem': 'Usuários retornados com sucesso'}, 200

    def post(self, user):
        if (database.main[self.collection].find_one({"email": user['email']}) != None):
            return {'resultado': False,
                    'mensagem': 'Erro ao criar usuário. Já existe um usuário com esse email'}, 409

        user['senha'] = generate_password_hash(user['senha'])
        database.main[self.collection].insert_one(user)
        return {'resultado': True,
                'mensagem': 'Usuário criado com sucesso'}, 201

    def put(self, user, current_user):
        old_user = database.main[self.collection].find_one(
            {'_id':  ObjectId(user['id'])})

        if not old_user:
            return {'resultado': {},
                    'mensagem': 'Erro ao atualizar usuário. Usuário não encontrado'}, 404

        if str(old_user['_id']) != current_user['id']:
            return {'resultado': {},
                    'mensagem': 'Erro ao atualizar usuário. Você não tem permissão para alterar este usuário'}, 401

        updated_user = old_user
        updated_user['nome'] = user['nome']
        updated_user['telefone'] = user['telefone']
        updated_user['endereco'] = user['endereco']
        my_query = {'_id':  ObjectId(user['id'])}
        new_values = {'$set': updated_user}
        database.main[self.collection].update_one(my_query, new_values)
        return {'resultado': self.entity_response(updated_user),
                'mensagem': 'Usuário alterado com sucesso'}, 200

    def delete(self, id, current_user):
        user = database.main[self.collection].find_one({'_id':  ObjectId(id)})
        if not user:
            return {
                "resultado": False,
                "mensagem": "Erro ao apagar usuário. Não foi possível encontrar este usuário"
            }, 404

        if str(user['_id']) != current_user['id']:
            return {
                "resultado": False,
                "mensagem": "Erro ao apagar usuário. Estas informações pertencem à outro usuário"
            }, 401

        database.main[self.collection].delete_one({'_id':  ObjectId(id)})

        return {
            "resultado": True,
            "mensagem": "usuário deletado com sucesso"
        }, 204

    def get_one(self, id, current_user):
        user = database.main[self.collection].find_one({'_id':  ObjectId(id)})
        if not user:
            return {'resultado': None,
                    'mensagem': 'Não foi possível encontrar este usuário'}, 404

        return {'resultado': self.entity_response(user),
                'mensagem': 'Usuário retornado com sucesso'}, 200

    def get_users_by_name(self, name, current_user):
        users = list(database.main[self.collection].find({'nome': name}))
        if not users:
            return {'resultado': None,
                    'mensagem': 'Não foi possível buscar usuários'}, 404

        return {'resultado': self.entity_response_list(users),
                'mensagem': 'Usuários retornados com sucesso'}, 200

    def verify_password(self, email, password):
        user = database.main[self.collection].find_one({'email':  email})
        if not user:
            return {'resultado': False,
                    'token': 'null',
                    'mensagem': 'Email não cadastrado'}, 404

        if not check_password_hash(user['senha'], password):
            return {'resultado': False,
                    'token': 'null',
                    'mensagem': 'Senha inválida'}, 401
        payload = {
            "id": str(user['_id']),
            "nome": user['nome']
        }

        token = encode(payload, var_env.secret_key)

        return {'resultado': True,
                'token': token,
                'mensagem': 'Senha verificada'}, 202

    def change_password(self, email, old_password, new_password, current_user):
        valid_old_password = self.verify_password(email, old_password)
        if valid_old_password[0]['resultado']:
            user = database.main[self.collection].find_one({'email':  email})
            if str(user['_id']) != current_user['id']:
                return {'resultado': False,
                        'mensagem': 'Você não tem permissão para alterar este dado'}, 401

            user['senha'] = generate_password_hash(new_password)
            my_query = {'email':  email}
            new_values = {'$set': user}
            database.main[self.collection].update_one(my_query, new_values)
            return {'resultado': True,
                    'mensagem': 'Senha alterada com sucesso'}, 200

        if valid_old_password[0]['mensagem'] == 'Senha inválida':
            return {'resultado': False,
                    'mensagem': 'Senha antiga é inválida'}, 401
        if valid_old_password[0]['mensagem'] == 'Email não cadastrado':
            return {'resultado': False,
                    'mensagem': 'Email não cadastrado'}, 404

    def get_users_by_email(self, email, current_user):
        user = database.main[self.collection].find_one({"email": email})
        if not user:
            return {'resultado': None,
                    'mensagem': 'Não foi possível buscar usuários'}, 404
        if str(user['_id']) != current_user['id']:
            return {'resultado': False,
                    'mensagem': 'Você não tem permissão para acessar este dado'}, 401
        return {'resultado': self.entity_response(user),
                'mensagem': 'Usuários retornados com sucesso'}, 200

    def get_user_by_id(self, id):

        user = self.entity_response(
            database.main[self.collection].find_one({'_id':  ObjectId(id)}))
        return user

    def send_email(self, user):
        user_db = database.main[self.collection].find_one(
            {"email": user['email']})
        if not user_db:
            return {'resultado': "A conta com esse email não foi encontrada"}, 404
        if user['numero'] != user_db['endereco']['numero'] or user['cep'] != user_db['endereco']['cep'] or user['cidade'] != user_db['endereco']['cidade'] or user['telefone'] != user_db['telefone']:
            return {'resultado': "Uma ou mais informações estão erradas"}, 401

        message = """Content-Type: text/plain
                    Subject: Redefinição de senha de Feira Kit
                    Olá {nome}, a sua senha foi redefinida com sucesso, o seu novo login no aplicativo é:
                    Usuário: {usuario} 
                    Senha: {senha}
                    Aviso: Esta é uma senha gerada automaticamente, recomendamos que você faça a alteração da sua senha pelo aplicativo acessando 'Minha Conta' > 'Alterar Senha'.
                    att. Equipe Feira Kit 
                    """.format(nome=user_db['nome'], usuario=user['email'], senha=senha).encode(encoding="utf-8", errors='strict')

        senha = str(secrets.token_hex(6))
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(var_env.email, var_env.senha)
        server.sendmail(var_env.email, user['email'], message)
        server.quit()

        user_db['senha'] = generate_password_hash(senha)
        my_query = {'email':  user['email']}
        new_values = {'$set': user_db}
        database.main[self.collection].update_one(my_query, new_values)
        return {'resultado': "email enviado"}, 201


user_service = User()
