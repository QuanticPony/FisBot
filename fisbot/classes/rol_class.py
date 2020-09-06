import discord
from discord.ext import commands
import asyncio
from random import randint
from .user_class import FisUser
from .display_class import Display

class FisRol(Display):

    from ..database.roles import RolesDB
    database = RolesDB()


    def __init__(self, rol_id=0, level=0, description='None', privileges='None'):
        super().__init__(role=True)
        self.id = rol_id
        self.name = ''
        self.level = level
        self.description = description
        self.privileges = privileges
        
        #self.database = RolesDB()




# Funciones de la clase FisRol



    def new_rol(self, user: FisUser) -> FisRol:
        '''Devuelve el rol `FisRol` que deberia tener el usuario especificado. Si no hay un rol para ese nivel devuelve `None`'''

        return self.database.get_rol(user.level)



    def prev_rol(self, level) -> FisRol:
        '''Devuelve el ultimo rol `FisRol` que consiguio el usuario. Devuelve `None` si no ha conseguido nunca un rol'''


        for i in reversed(range(0, level - 1)):
            rol = self.database.get_rol()
            if rol: 
                return rol
        else:
            return None


    @self.check_if_context()
    async def remove_from(self, user: FisUser) -> bool:
        '''Elimina del usuario `user` el rol. Devuelve `true`si lo consigue y `false` si no'''
        
        disc_user = self._ctx.guild.get_member(user.id)
        disc_rol = self._ctx.guild.get_role(self.id)
        if disc_user and disc_rol:
            if disc_rol not in disc_user.roles: 
                new_roles = disc_user.roles
                new_roles.remove(disc_rol)
                try:
                    await disc_user.edit(roles=new_roles)
                    return True
                except:
                    return False
        else:
            return False


    @self.check_if_context()
    async def next_rol(self, user: FisUser):
        '''Da al usuario su siguiente rol si es necesario'''

        disc_user = self._ctx.guild.get_member(user.id)
        disc_rol = self._ctx.guild.get_role(self.new_rol(user))
        if disc_user and disc_rol:
            if disc_rol not in disc_user.roles:
                new_roles = disc_user.roles
                new_roles.apend(disc_rol)
                try:
                    await disc_user.edit(roles=new_roles)
                    return True
                except:
                    return False
        else:
            return False


    @self.check_if_context()
    async def create_discord_obj(self, role_name) -> discord.Role:
        '''Crea un rol de discord a partir de un nombre y devuelve el `discord.Role`'''

        role = await self._ctx.guild.create_role(
            hoist=True, mentionable=True, name=role_name, 
            permissions=discord.Permissions.general(),
            colour=discord.Color.from_rgb(randint(0,255),randint(0,255),randint(0,255))
            )
        return role


# Funciones sobreescritas de la clase Display

    @self.check_if_context()
    def discord_obj(self) -> discord.Role:

        self._disc_obj = self._ctx.guild.get_role(self.id)

        if not self._disc_obj:
            self.create_discord_obj(self._ctx)

        self.name = self._disc_obj.name
        return self._disc_obj


    def save_in_database(self, func) -> bool:
        return self.database.update_rol(self)



    def title_for_new(self) -> str:

        return 'Crear rol personalizado'

    def title_for_mod(self) -> str:

        return f"Modificar {self.name}"

    def title_for_del(self) -> str:
        return f"Eliminar {self.name} id= {self.id}"


    def description_for_new(self) -> str:

            return '''Abajo tienes la lista de todos los campos modificables. 
        Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
        *Cuando hayas acabado* presiona el boton de guardar'''
        

    def description_for_mod(self) -> str:

            return '''Abajo tienes la lista de todos los campos modificables. 
        Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
        *Cuando hayas acabado* presiona el boton de guardar'''

    def description_for_del(self) -> str:

        return  '''¿Seguro que quiere eliminar este elemento de la base de datos y de discord?
        Si es así, reaccione ✅. De lo contrario, reaccione ❌:'''