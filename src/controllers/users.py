from flask_restx import Resource
from src.server.instance import server
from src.models.user import user_response, user_request, user_update_request
from src.service.user import user_service

app, api = server.app, server.api.namespace('users',
                                            description='Recurso de usuários')
@api.route('')
class User(Resource):
    @api.marshal_list_with(user_response)
    def get(self):
        users = user_service.get()
        return users, 200
    
    @api.expect(user_request, validate=True)
    @api.marshal_with(user_response)
    def post(self):
        user = user_service.post(api.payload)
        return user, 201
    
    @api.expect(user_update_request, validate=True)
    @api.marshal_with(user_response)
    def put(self):
        response = user_service.put(api.payload)
        return response, 204