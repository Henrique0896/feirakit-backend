from functools import wraps
import jwt
from flask import request,current_app
from src.service.user import user_service
import os
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())

def jwt_required(f):
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
            secret=os.getenv("SECRET_KEY")
            decoded=jwt.decode(token_pure,secret,algorithms=["HS256"])
            current_user=user_service.get_one(decoded['id'])['resultado']
        except:
           return {"error":"O token é inválido"},403
        
        return f(current_user=current_user,*args,*kwargs)
    
       
    return wrapper