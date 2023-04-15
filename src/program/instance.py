from flask import Flask
from flask_restx import Api
from src.core.settings_env import settings_env
class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.setdefault("RESTX_MASK_SWAGGER", False)
        self.app.config['SECRET_KEY'] = [settings_env.get_var("SECRET_KEY")]
        self.api = Api(self.app,
                       version='1.0',
                       title='Feirakit API',
                       description='',
                       doc='/swagger',
                       authorizations={
                             'Bearer': {
                                 'type': 'apiKey',
                                 'in': 'header',
                                 'name': 'Authorization'
                             }
                       }
                       )

    def run(self):
        self.app.run(
            debug=True,
            host='0.0.0.0', port=5000
        )


server = Server()
