from flask_restx import fields
from src.program.instance import server

types_response = server.api.model('Units', {
    'units': fields.List(fields.String),
    'categories': fields.List(fields.String)
})