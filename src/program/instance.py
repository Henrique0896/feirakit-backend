from flask import Flask
from flask_restx import Api
import os
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv())


class Server():
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config.setdefault("RESTX_MASK_SWAGGER", False)
        self.app.config['SECRET_KEY'] = [os.getenv("SECRET_KEY")]
        self.api = Api(self.app,
                       version='1.0',
                       title='Feirakit API',
                       description='',
                       doc='/swagger'
                       )

    def run(self):
        self.app.run(
            debug=True,
            host='0.0.0.0', port=5000
        )


server = Server()
