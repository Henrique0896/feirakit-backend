from flask_restx import Resource
from src.program.instance import server
from src.models.product import product_response, product_request, product_update_request,product_response_default,product_update_response
from src.models.id import id_request
from src.service.product import product_service
from src.models.product_types import types_response
from src.controllers.authenticate import jwt_required
from flask import request


app, api = server.app, server.api.namespace('products',description='Recurso de produtos')
@api.route('')
class Product(Resource):
    @api.marshal_list_with(product_response)
    @api.doc(params={'page': 'Index of page','limit':'Quantity of products by request','sort':'order of results (1=asc / -1= dec)'})
    def get(self):
        page= request.args.get('page',type=int,default=1)
        limit= request.args.get('limit',type=int ,default=10)
        sort= request.args.get('sort',type=int ,default=1)
        products = product_service.get(page,limit,sort)
        return products, 200

    @api.expect(product_request, validate=True)
    @jwt_required
    @api.marshal_with(product_response_default)
    @api.doc(security='Bearer')
    def post(self,current_user):
        response = product_service.post(api.payload,current_user)
        return response

    @api.expect(product_update_request)
    @jwt_required
    @api.marshal_with(product_update_response)
    @api.doc(security='Bearer')
    def put(self,current_user):
        response = product_service.put(api.payload,current_user)
        return response

    @api.expect(id_request, validate=True)
    @jwt_required
    @api.marshal_with(product_response_default)
    @api.doc(security='Bearer')
    def delete(self,current_user):
        response = product_service.delete(api.payload['id'],current_user)
        return response

@api.route('/<string:id>')
class ProductSeachById(Resource):
    @api.marshal_list_with(product_response)
    def get(self, id):
        products = product_service.get_one(id)
        return products, 200
        
@api.route('/byname/<string:name>')
class ProductSeachByName(Resource):
    @api.marshal_list_with(product_response)
    def get(self, name):
        products = product_service.get_products_by_name(name)
        return products, 200

@api.route('/by-id-usuario/<string:id_usuario>')
class ProductSeachByNameOfUsuario(Resource):
    @api.marshal_list_with(product_response)
    def get(self, id_usuario):
        products = product_service.get_products_by_id_usuario(id_usuario)
        return products, 200

@api.route('/units')
class GetUnity(Resource):
    @api.marshal_with(types_response)
    def get(self):
        product_types = product_service.get_product_types()
        return product_types, 200