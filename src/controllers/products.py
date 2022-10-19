from flask_restx import Resource
from src.server.instance import server
from src.models.product import product
app, api = server.app, server.api

products_db = [
    {
        "id": 0, "title": "Test"
    },
    {
        "id": 1, "title": "Test"
    }
]

@api.route('/products')
class ProductList(Resource):
    @api.marshal_list_with(product)
    def get(self):
        return products_db
        
    @api.expect(product, validate=True)
    @api.marshal_list_with(product)
    def post(self):
        response = api.payload
        products_db.append(response)
        return response, 200