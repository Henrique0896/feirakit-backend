from src.program.instance import server
from src.controllers.products import Product, ProductSeachById, ProductSeachByName, ProductSeachByNameOfUsuario
from src.controllers.users import User

server.run()