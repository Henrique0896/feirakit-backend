from flask_restx import Resource
from src.server.instance import server
from src.models.receita import receita_response, receita_request, receita_update_request
from src.models.id import id_request
from src.service.receita import receita_service


app, api = server.app, server.api.namespace('receitas',description='Recurso de produtos')
@api.route('')
class Receita(Resource):
    @api.marshal_list_with(receita_response)
    def get(self):
        receitas = receita_service.get()
        return receitas, 200

    @api.expect(receita_request, validate=True)
    @api.marshal_list_with(receita_request)
    def post(self):
        receita = receita_service.post(api.payload)
        return receita, 201

    @api.expect(receita_update_request)
    @api.marshal_with(receita_response)
    def put(self):
        response = receita_service.put(api.payload)
        return response, 204

    @api.expect(id_request, validate=True)
    @api.response(204, 'Receita deleted')
    def delete(self):
        receita = receita_service.delete(api.payload['id'])
        return receita, 204