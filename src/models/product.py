from flask_restx import fields
from src.server.instance import server
from src.models.id import id

product_request = server.api.model('ProductRequest',  {
    'title': fields.String(required=True, min_Length=1, max_Length=200, description='Título do produto')
})

product_response = server.api.inherit('ProductResponse', product_request, id)