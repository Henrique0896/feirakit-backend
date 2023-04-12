from flask_restx import Resource
from src.program.instance import server
from src.models.products import product_response, product_request, product_update_request
from src.models.ids import id_request
from src.service.products import product_service
from src.models.product_types import types_response

app, api = server.app, server.api.namespace('products',description='Recurso de produtos')
@api.route('')
class Product(Resource):
    @api.marshal_list_with(product_response)
    def get(self):
        products = product_service.get()
        return products, 200

    @api.expect(product_request, validate=True)
    @api.marshal_list_with(product_request)
    def post(self):
        product = product_service.post(api.payload)
        return product, 201

    @api.expect(product_update_request)
    @api.marshal_with(product_response)
    def put(self):
        response = product_service.put(api.payload)
        return response, 204

    @api.expect(id_request, validate=True)
    @api.response(204, 'Product deleted')
    def delete(self):
        product = product_service.delete(api.payload['id'])
        return product, 204

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

@api.route('/by-id-user/<string:id_user>')
class ProductSeachByNameOfUser(Resource):
    @api.marshal_list_with(product_response)
    def get(self, id_user):
        products = product_service.get_products_by_id_user(id_user)
        return products, 200

@api.route('/units')
class GetUnity(Resource):
    @api.marshal_with(types_response)
    def get(self):
        product_types = product_service.get_product_types()
        return product_types, 200
        