from flask_restx import fields
from src.server.instance import server
from src.models.id import id

kit_request = server.api.model('kit',  {
    'nome': fields.String(required=True, min_Length=1, max_Length=200, description='Nome do kit'),
    'descricao': fields.String(required=True, min_Length=1, max_Length=200, description='Descrição do kit'),
    'preco': fields.Integer(required=True, description='Preço do kit'),
    'conteudo': fields.String(required=True, description='O que vem no kit'),
    'receitas': fields.String(required=True, description='Receitas possiveis com esse kit')
})
kit_response = server.api.inherit('kitResponse', kit_request, id)
kit_update_request = server.api.inherit('kitUpdateRequest',  kit_request, id)
