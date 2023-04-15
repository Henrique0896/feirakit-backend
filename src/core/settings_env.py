from dotenv import load_dotenv, find_dotenv
from os import getenv

class SettingsEnv():
    def __init__(self):
        self.load_vars_env()
    
    def load_vars_env(self):
        load_dotenv(find_dotenv())

    def get_var(self, var_name):
        return getenv(var_name)

settings_env = SettingsEnv()