from flask_restx import fields
from src.program.instance import server
from src.models.id import id

endereco = server.api.model('Endereco', {
 'rua': fields.String(required=True, min_Length=3, max_Length=200, description='Rua'),
 'numero': fields.String(required=True, min_Length=1, max_Length=1000, description='Numero'),
 'bairro': fields.String(required=True, min_Length=3, max_Length=200, description='Bairro'),
 'cep': fields.String(required=True, min_Length=8, max_Length=8, description='CEP'),
 'complemento': fields.String(required=True, min_Length=3, max_Length=200, description='Complemento'),
 'cidade': fields.String(required=True, min_Length=3, max_Length=200, description='Cidade')  
})

user_request = server.api.model('UserRequest',  {
    'nome': fields.String(required=True, min_Length=3, max_Length=200, description='Nome completo do usuário'),
    'email': fields.String(required=True, min_Length=5, max_Length=200, description='Email'),
    'telefone': fields.String(required=True, min_Length=6, max_Length=20, description='Telefone'),
    'senha': fields.String(required=True, min_Length=4, max_Length=200, description='Senha'),
    'endereco': fields.Nested(endereco)
})

user_response = server.api.inherit('UserResponse', user_request, id)
user_update_request = server.api.inherit('userUpdateRequest',  user_request, id)