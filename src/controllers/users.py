from flask_restx import Resource
from src.server.instance import server
from src.models.user import user_response, user_request, user_update_request
from src.models.id import id_request
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

    @api.expect(id_request, validate=True)
    @api.response(204, 'User deleted')
    def delete(self):
        response = user_service.delete(api.payload['id'])
        return response, 204
    
@api.route('/<string:id>')
class UserSeachById(Resource):
    @api.marshal_list_with(user_response)
    def get(self, id):
        user = user_service.get_one(id)
        return user, 200
        
@api.route('/byname/<string:name>')
class UserSeachByName(Resource):
    @api.marshal_list_with(user_response)
    def get(self, name):
        users = user_service.get_users_by_name(name)
        return users, 200
