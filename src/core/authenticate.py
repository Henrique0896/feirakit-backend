from flask import request
from functools import wraps
from jwt import decode
from src.core.settings_env import settings_env
from src.service.user import user_service

class Authenticate():
    def jwt_required(self, f):
        @wraps(f)
        def wrapper(*args,**kwargs):
            token=None
            if 'Authorization'in request.headers:
                token= request.headers['Authorization']
            
            if not token:
                return {"error":"Você não tem permissão para acessar este recurso."},403
            
            if not "Bearer" in token:
                return {"error":"Token inválido"},401

            try:
                token_pure= token.replace("Bearer ","")
                secret = settings_env.get_var("SECRET_KEY")
                decoded= decode(token_pure,secret,algorithms=["HS256"])
                current_user=user_service.get_one(decoded['id'])['resultado']
            except:
                return {"error":"O token é inválido"},403
            
            return f(current_user=current_user,*args,*kwargs)
        return wrapper
    
authenticate = Authenticate()