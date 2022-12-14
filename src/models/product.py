from flask_restx import fields
from src.server.instance import server
from src.models.id import id
from src.models.enums import unidade_enum, avaliacao_enum, categoria_enum

product_request = server.api.model('Product',  {
    'nome_usuario': fields.String(required=True, min_Length=1, max_Length=200, description='Nome do usuario'),
    'nome': fields.String(required=True, min_Length=1, max_Length=200, description='Nome do produto'),
    'categoria': fields.String(required=True, enum=categoria_enum, description='Tipo de produto'),
    'descricao': fields.String(required=True, min_Length=1, max_Length=200, description='Descrição do produto'),
    'unidade': fields.String(required=True, enum=unidade_enum, description='Unidade do produto'),
    'estoque': fields.Integer(required=True, description='Quantidade no estoque'),
    'produtor': fields.String(required=True, min_Length=1, max_Length=50, description='Nome produtor'),
    'bestbefore': fields.Boolean(required=True, description='Produto colhido após a compra'),
    'validade': fields.Date(required=True, description='Validade do produto'),
    'desconto': fields.Integer(description='Porcentagem de desconto'),
    'avaliacao': fields.String(enum=avaliacao_enum, description='Avaliação dos clientes'),
    'comentarios': fields.String(description='Comentarios sobre o produto'),
    'preco': fields.Integer(description='valor do produto'),
    'imagem_url': fields.List(fields.String)
})

product_response = server.api.inherit('ProductResponse', product_request, id)

product_update_request = server.api.inherit('ProductUpdateRequest',  product_request, id)
