from flask_restx import fields
from src.program.instance import server

id =  {
    'id': fields.String(description='ID do registro', required=True),
}

id_request = server.api.model('Id', id )
