from flask_restx import fields
from src.server.instance import server
from src.models.id import id

user_request = server.api.model('UserRequest',  {
    'nome': fields.String(required=True, min_Length=3, max_Length=200, description='Nome completo do usuário'),
    'email': fields.String(required=True, min_Length=5, max_Length=200, description='Email'),
    'telefone': fields.String(required=True, min_Length=6, max_Length=20, description='Telefone'),
    'endereco': fields.String(required=True, min_Length=10, max_Length=200, description='Endereço (CEP, rua, numero, complemento, bairro, cidade, estado)'),
    'senha': fields.String(required=True, min_Length=4, max_Length=200, description='Senha'),
})

user_response = server.api.inherit('UserResponse', user_request, id)
user_update_request = server.api.inherit('userUpdateRequest',  user_request, id)