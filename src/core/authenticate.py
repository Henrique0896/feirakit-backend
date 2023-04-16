from flask import request
from bson import ObjectId
from functools import wraps
from jwt import decode
from src.program.database import database
from src.service.id_settings import IdSettings
from src.core.var_env import var_env

class Authenticate(IdSettings):
    def __init__(self):
        self.collection = 'user'
 
    def jwt_required(self, f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization']

            if not token:
                return {"error": "Você não tem permissão para acessar este recurso."}, 403

            if not "Bearer" in token:
                return {"error": "Token inválido"}, 401

            try:
                token_pure = token.replace("Bearer ", "")
                decoded = decode(token_pure, var_env.secret_key,
                                 algorithms=["HS256"])
                current_user=self.entity_response(database.main[self.collection].find_one({'_id':  ObjectId(decoded['id'])}))
            except:
                return {"error": "O token é inválido"}, 403

            return f(current_user=current_user, *args, *kwargs)
        return wrapper


authenticate = Authenticate()
