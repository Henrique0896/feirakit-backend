from flask_restx import Resource
from src.program.server import server
from src.models import user as user_model
from src.models.id import id_request
from src.service.user import user_service
from src.core.authenticate import authenticate
app, api = server.app, server.api.namespace('users',
                                            description='Recurso de usuários')

@api.route('')
class User(Resource):
    @authenticate.jwt_required
    @api.doc(security='Bearer')
    @api.marshal_with(user_model.response)
    def get(self,current_user):
        users = user_service.get()
        return users

    @api.expect(user_model.request, validate=True)
    @api.marshal_with(user_model.create_response)
    def post(self):
        user = user_service.post(api.payload)
        return user

    @api.expect(user_model.update_request, validate=True)
    @authenticate.jwt_required
    @api.marshal_with(user_model.updated_response)
    @api.doc(security='Bearer')
    def put(self, current_user):
        response = user_service.put(api.payload, current_user)
        return response

    @api.expect(id_request, validate=True)
    @authenticate.jwt_required
    @api.doc(security='Bearer')
    @api.marshal_with(user_model.response_default)
    def delete(self, current_user):
        response = user_service.delete(api.payload['id'], current_user)
        return response

@api.route('/<string:id>')
class UserSeachById(Resource):
    @authenticate.jwt_required
    @api.doc(security='Bearer')
    @api.marshal_list_with(user_model.response)
    def get(self, id):
        user = user_service.get_one(id)
        return user, 200

@api.route('/byemail/<string:email>')
class UserSeachByEmail(Resource):
    @authenticate.jwt_required
    @api.doc(security='Bearer')
    @api.marshal_with(user_model.response)
    def get(self, email):
        users = user_service.get_users_by_email(email)
        return users, 200

@api.route('/byname/<string:name>')
class UserSeachByName(Resource):
    @authenticate.jwt_required
    @api.doc(security='Bearer')
    @api.marshal_list_with(user_model.response)
    def get(self, name):
        users = user_service.get_users_by_name(name)
        return users, 200

@api.route('/check-password')
class CheckPassword(Resource):
    @api.expect(user_model.check_password_request, validate=True)
    @api.marshal_with(user_model.response_login_default)
    def post(self):
        valid_password = user_service.verify_password(
            api.payload['email'], api.payload['senha'])
        return valid_password
    
@api.route('/change-password')
class ChangePassword(Resource):
    @api.expect(user_model.change_password_request, validate=True)
    @authenticate.jwt_required
    @api.marshal_with(user_model.response_default)
    @api.doc(security='Bearer')
    def post(self, current_user):
        valid_password = user_service.change_password(
            api.payload['email'], api.payload['senha'], api.payload['nova_senha'], current_user)

        return valid_password
