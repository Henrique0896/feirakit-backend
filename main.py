from src.server.instance import server
from src.controllers.products import Product, ProductSeachById, ProductSeachByName, ProductSeachByNameOfUsuario
from src.controllers.users import User
from src.controllers.kits import kit
from src.controllers.receitas import Receita


server.run()