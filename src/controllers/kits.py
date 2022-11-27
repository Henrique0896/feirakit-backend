from flask_restx import Resource
from src.server.instance import server
from src.models.id import id_request
from src.models.kit import kit_response, kit_request, kit_update_request
from src.service.kit import kit_service

app, api = server.app, server.api.namespace('kits', description='Recurso de usuários')
@api.route('')
class kit(Resource):
    @api.marshal_list_with(kit_response)
    def get(self):
        kits = kit_service.get()
        return kits, 200
    
    @api.expect(kit_request, validate=True)
    @api.marshal_with(kit_response)
    def post(self):
        kit = kit_service.post(api.payload)
        return kit, 201

    @api.expect(kit_update_request)
    @api.marshal_with(kit_response)
    def put(self):
        response = kit_service.put(api.payload)
        return response, 204

    @api.expect(id_request, validate=True)
    @api.response(204, 'kit deleted')
    def delete(self):
        kit = kit_service.delete(api.payload['id'])
        return kit, 204
