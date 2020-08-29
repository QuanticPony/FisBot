import discord
from .user_class import FisUser

class FisRol():

    def __init__(self, rol_id=0, level=0, description='', privileges=''):
        self.rol_id = rol_id
        self.level = level
        self.description = description
        self.privileges = privileges
        from ..database.roles import RolesDB
        self.database = RolesDB()


    def new_rol(self, user: FisUser) -> FisRol:
        return self.database.get_rol(user.level)