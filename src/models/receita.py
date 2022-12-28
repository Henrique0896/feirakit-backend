from flask_restx import fields
from src.server.instance import server
from src.models.id import id

receita_request = server.api.model('Receita',  {
    'possiveis_receitas': fields.List(fields.String),
    'nome_receitas': fields.String(required=True, min_Length=1, max_Length=200, description='Nome da receita'),

})

receita_response = server.api.inherit('ReceitaResponse', receita_request, id)

receita_update_request = server.api.inherit('ReceitaUpdateRequest',  receita_request, id)
