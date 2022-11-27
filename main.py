from src.server.instance import server
from src.controllers.products import Product, ProductSeachById, ProductSeachByName
from src.controllers.users import User
from src.controllers.kits import kit


server.run()