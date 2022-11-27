from flask_restx import fields
from src.server.instance import server
from src.models.id import id


user_request = server.api.model('ProductRequest',  {
    'nome_completo': fields.String(required=True, min_Length=1, max_Length=200, description='Nome do usuário'),
    'email': fields.String(required=True, min_Length=1, max_Length=200, description='Email'),
    'telefone': fields.String(required=True, min_Length=1, max_Length=15, description='Telefone'),
})

user_response = server.api.inherit('UserResponse', user_request, id)

user_update_request = server.api.inherit('userUpdateRequest',  user_request, id)