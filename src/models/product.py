from flask_restx import fields
from src.server.instance import server

product = server.api.model('Product', {
    'id': fields.String(description='ID do registro'),
    'title': fields.String(required=True, min_Length=1, max_Length=200, description='Título do produto')
})

