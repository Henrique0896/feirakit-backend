from flask_restx import fields
from src.server.instance import server
from src.models.id import id

product_request = server.api.model('ProductRequest',  {
    'nome': fields.String(required=True, min_Length=1, max_Length=200, description='Nome do produto'),
    'categoria': fields.String(required=True, min_Length=1, max_Length=200, description='Tipo de produto'),
    'descricao': fields.String(required=True, min_Length=1, max_Length=200, description='Descrição do produto'),
    'unidade': fields.String(required=True, min_Length=1, max_Length=200, description='Unidade do produto'),
    'estoque': fields.Integer(required=True, min_Length=1, max_Length=5, description='Quantidade no estoque'),
    'produtor': fields.String(required=True, min_Length=1, max_Length=50, description='Nome produtor'),
    'bestbefore': fields.Boolean(required=None, min_Length=1, max_Length=5, description='Produto colhido após a compra'),
    'validade': fields.Date(required=True, description='Validade do produto'),
    'desconto': fields.Integer(required=True, min_Length=1, max_Length=2, description='Porcentagem de desconto'),
    'avaliacao': fields.Integer(required=True, min_Length=1, max_Length=5, description='Avaliação dos clientes'),
    'comentarios': fields.String(required=True, min_Length=1, max_Length=200, description='Comentarios sobre o produto')

})

product_response = server.api.inherit('ProductResponse', product_request, id)

product_update_request = server.api.inherit('ProductUpdateResponse',  product_request, id)