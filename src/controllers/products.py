from itertools import product
from urllib import response
from flask_restx import Resource
from src.server.instance import server
from src.models.product import product_response, product_request, product_update_request
from src.models.id import id_request
from src.service.product import product_service

app, api = server.app, server.api
@api.route('/products')
class ProductList(Resource):
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