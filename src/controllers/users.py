from flask_restx import Resource
from src.server.instance import server
from src.models.user import user_response


app, api = server.app, server.api.namespace('users',
                                            description='Recurso de usuários')
@api.route('')
class User(Resource):
    @api.marshal_list_with(user_response)
    def get(self):
        return {'id': '1', 'nome': 'teste'}, 200