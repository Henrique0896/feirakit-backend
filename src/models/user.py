from flask_restx import fields
from src.server.instance import server
from src.models.id import id


user_request = server.api.model('ProductRequest',  {
    'nome': fields.String(required=True, min_Length=1, max_Length=200, description='Nome do usuário'),
})

user_response = server.api.inherit('UserResponse', user_request, id)