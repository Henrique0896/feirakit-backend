from dotenv import load_dotenv, find_dotenv
from os import getenv

class VarEnvs():
    def __init__(self):
        load_dotenv(find_dotenv())
        self.secret_key = getenv("SECRET_KEY")
        self.database = getenv("DATABASE")
        self.db_connection = getenv("DB_CONNECTION")
        self.port = int(getenv("PORT"))
        self.email = str(getenv("EMAIL"))
        self.senha = str(getenv("APPSENHA"))

var_env = VarEnvs()
