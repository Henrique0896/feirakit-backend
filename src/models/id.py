from flask_restx import fields
from src.server.instance import server

id =  {
    'id': fields.String(description='ID do registro', required=True),
}

id_request = server.api.model('Id', id )
