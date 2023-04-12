from flask_restx import fields
from src.program.instance import server
from src.models.ids import id
from src.models.enums import units_enum, categories_enum

product_request = server.api.model('Product',  {
    'productor_id': fields.String(required=True, min_Length=1, max_Length=200, description='Produtor'),
    'name_product': fields.String(required=True, min_Length=1, max_Length=200, description='Nome do produto'),
    'category': fields.String(required=True, enum=categories_enum, description='Tipo de produto'),
    'description': fields.String(required=True, min_Length=1, max_Length=200, description='Descrição do produto'),
    'unity': fields.String(required=True, enum=units_enum, description='Unidade do produto'),
    'stock': fields.Integer(required=True, description='Quantidade no estoque'),
    'bestbefore': fields.Boolean(required=True, description='Produto colhido após a compra'),
    'validity': fields.Date(required=True, description='Validade do produto'),
    'discount': fields.Integer(description='Porcentagem de desconto'),   
    'image_url': fields.List(fields.String),
    'price': fields.Float(description='valor do produto'),
})

product_response = server.api.inherit('ProductResponse', product_request, id)

product_update_request = server.api.inherit('ProductUpdateRequest',  product_request, id)
