from flask_restx import fields
from src.program.instance import server
from src.models.ids import id

address = server.api.model('Address', {
 'street': fields.String(required=True, min_Length=3, max_Length=200, description='Rua'),
 'number': fields.String(required=True, min_Length=1, max_Length=1000, description='Numero'),
 'neighborhood': fields.String(required=True, min_Length=3, max_Length=200, description='Bairro'),
 'cep': fields.String(required=True, min_Length=8, max_Length=8, description='CEP'),
 'complement': fields.String(required=True, min_Length=3, max_Length=200, description='Complemento'),
 'city': fields.String(required=True, min_Length=3, max_Length=200, description='Cidade'),
  'state': fields.String(required=True, min_Length=3, max_Length=200, description='Estado')
})

user = server.api.model('User', {
    'name': fields.String(required=True, min_Length=3, max_Length=200, description='Nome completo do usuário'),
    'email': fields.String(required=True, min_Length=5, max_Length=200, description='Email'),
    'phone_number': fields.String(required=True, min_Length=6, max_Length=20, description='Telefone'),
    'adress': fields.Nested(address)
})

user_request = server.api.model('UserRequest',  {
    'name': fields.String(required=True, min_Length=3, max_Length=200, description='Nome completo do usuário'),
    'email': fields.String(required=True, min_Length=5, max_Length=200, description='Email'),
    'phone_number': fields.String(required=True, min_Length=6, max_Length=20, description='Telefone'),
    'password': fields.String(required=True, min_Length=4, max_Length=200, description='Senha'),
    'adress': fields.Nested(address)
})

user_response = server.api.model('UserResponse',  {
    'result': fields.List(fields.Nested(server.api.inherit('userResponse',  user, id))),
    'message': fields.String(),
})

user_create_response = server.api.model('UserCreateResponse',  {
    'result': fields.Boolean(),
    'message': fields.String(),
})

user_update_request = server.api.inherit('userUpdateRequest',  server.api.model('userUpdateRequestProps',  {
    'name': fields.String(required=True, min_Length=3, max_Length=200, description='Nome completo do usuário'),
    'phone_number': fields.String(required=True, min_Length=6, max_Length=20, description='Telefone'),
    'adress': fields.Nested(address)
}), id)

check_password_request = server.api.model('checkPasswordRequest',  {
    'email': fields.String(required=True, min_Length=5, max_Length=200, description='Email'),
    'password': fields.String(required=True, min_Length=4, max_Length=200, description='Senha a ser verificada'),
})

change_password_request = server.api.model('changePasswordRequest',  {
    'email': fields.String(required=True, min_Length=5, max_Length=200, description='Email'),
    'password': fields.String(required=True, min_Length=4, max_Length=200, description='Senha antiga'),
    'new_password': fields.String(required=True, min_Length=4, max_Length=200, description='Nova senha'),
})

response_default = server.api.model('responseDefault',  {
    'result': fields.Boolean(),
    'message': fields.String(),
})