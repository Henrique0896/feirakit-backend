from flask_restx import Resource
from src.program.instance import server
from src.models.user import user_response, user_request, user_update_request, check_password_request, change_password_request, response_default, user_create_response
from src.models.id import id_request
from src.service.user import user_service
from src.controllers.authenticate import jwt_required
app, api = server.app, server.api.namespace('users',
                                            description='Recurso de usuários')

@api.route('')
class User(Resource):
    @api.marshal_with(user_response)
    def get(self):
        users = user_service.get()
        return users, 200
    
    @api.expect(user_request, validate=True)
    @api.marshal_with(user_create_response)
    def post(self):
        user = user_service.post(api.payload)
        return user, 201
    
    @api.expect(user_update_request, validate=True)
    @jwt_required
    @api.marshal_with(user_response)
    @api.doc(security='apikey')
    def put(self,current_user):
        response = user_service.put(api.payload,current_user)
        return response, 204

    @api.expect(id_request, validate=True)
    @jwt_required
    @api.response(204, 'User deleted')
    @api.doc(security='apikey')
    @api.header('Authorization','JWT TOKEN')
    def delete(self,current_user):
        response = user_service.delete(api.payload['id'],current_user)
        return response, 204
    
@api.route('/<string:id>')
class UserSeachById(Resource):
    @api.marshal_list_with(user_response)
    def get(self, id):
        user = user_service.get_one(id)
        return user, 200

@api.route('/byemail/<string:email>')
class UserSeachByEmail(Resource):
    @api.marshal_with(user_response)
    def get(self, email):
        users = user_service.get_users_by_email(email)
        return users, 200
        
@api.route('/byname/<string:name>')
class UserSeachByName(Resource):
    @api.marshal_list_with(user_response)
    def get(self, name):
        users = user_service.get_users_by_name(name)
        return users, 200

@api.route('/check-password')
class CheckPassword(Resource):
    @api.expect(check_password_request, validate=True)
    @api.marshal_with(response_default)
    def post(self):
        valid_password = user_service.verify_password(api.payload['email'], api.payload['senha'])
        return valid_password, 200

@api.route('/change-password')
class ChangePassword(Resource):
    @api.expect(change_password_request, validate=True)
    @jwt_required
    @api.marshal_with(response_default)
    @api.doc(security='apikey')
    def post(self,current_user):
        valid_password = user_service.change_password(api.payload['email'], api.payload['senha'], api.payload['nova_senha'],current_user)
        return valid_password, 200
    