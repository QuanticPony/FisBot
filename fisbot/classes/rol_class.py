import discord
from discord.ext import commands
import asyncio
from random import randint
from .user_class import FisUser
from .display_class import Display

class FisRol(Display):

    _title_for_new = 'Crear rol personalizado'
    _title_for_mod = 'Modificar {0.name}'
    _title_for_del = 'Eliminar {0.name} id= {0.id}'

    _descr_for_new ='''Abajo tienes la lista de todos los campos modificables. 
        Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
        *Cuando hayas acabado* presiona el boton de guardar'''
    _descr_for_mod ='''Abajo tienes la lista de todos los campos modificables. 
        Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
        *Cuando hayas acabado* presiona el boton de guardar'''
    _descr_for_del ='''¿Seguro que quiere eliminar este elemento de la base de datos y de discord?
        Si es así, reaccione ✅. De lo contrario, reaccione ❌:'''


    def __init__(self, rol_id=0, level=0, description='None', privileges='None', context=None):
        self.id = rol_id
        self.name = ''
        self.level = level
        self.description = description
        self.privileges = privileges

        from ..database.roles import RolesDB
        self.database = RolesDB()

        if context:
            super().__init__(context, role=True)

    # TODO:
    def init_with_discord(self):
        self.name = 'None'

    
    def set_context(self, ctx):
        super().__init__(ctx, role=True)

# Funciones de la clase FisRol

    def new_rol(self, user: FisUser):
        '''Devuelve el rol `FisRol` que deberia tener el usuario especificado. Si no hay un rol para ese nivel devuelve `None`'''

        return self.database.get_rol(user.level)

    def prev_rol(self, level):
        '''Devuelve el ultimo rol `FisRol` que consiguio el usuario. Devuelve `None` si no ha conseguido nunca un rol'''


        for i in reversed(range(0, level - 1)):
            rol = self.database.get_rol()
            if rol: 
                return rol
        else:
            return None

    @Display.check_if_context
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

    @Display.check_if_context
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

    @Display.check_if_context
    async def create_discord_obj(self, role_name) -> discord.Role:
        '''Crea un rol de discord a partir de un nombre y devuelve el `discord.Role`'''

        role = await self._ctx.guild.create_role(
            hoist=True, mentionable=True, name=role_name, 
            permissions=discord.Permissions.general(),
            colour=discord.Color.from_rgb(randint(0,255),randint(0,255),randint(0,255))
            )
        return role

# Funciones sobreescritas de la clase Display

    @Display.prepare_dicts
    @Display.check_if_discord_obj
    def embed_show(self):
        '''Devuelve un `discord.Embed` que muestra el rol personalizado'''

        embed = discord.Embed(
            title=self.name,
            description=self._disc_obj.mention,
            colour=discord.Color.blue()
        )
        embed.add_field(
            name=f'Nivel requerido: {self.level}',
            value=self.description,
            inline=False
        )
        embed.add_field(
            name='Privilegios:',
            value=self.privileges,
            inline=False
        )
        return embed

    @Display.check_if_context
    def discord_obj(self) -> discord.Role:

        self._disc_obj = self._ctx.guild.get_role(self.id)

        if not self._disc_obj:
            self.create_discord_obj(self._ctx)

        self.name = self._disc_obj.name
        return self._disc_obj

    @Display.check_if_discord_obj
    def save_in_database(self, func) -> bool:

        return self.database.update_rol(self)

    def remove_from_database(self) -> bool:

        return self.database.del_rol(self)


    
    def title_for_new(self) -> str:

        return self._title_for_new.format(self)

    def title_for_mod(self) -> str:

        return self._title_for_mod.format(self)

    def title_for_del(self) -> str:
        return self._title_for_del.format(self)


    def description_for_new(self) -> str:

            return self._descr_for_new.format(self)

    def description_for_mod(self) -> str:

            return self._descr_for_mod.format(self)

    def description_for_del(self) -> str:

        return  self._descr_for_del.format(self)

    def prepare_atributes_dic(self):
        '''Prepara los diccionarios internos para trabajar con ellos'''


        self._atributes_dic = self.__dict__.copy()

        for key in ['id', 'database']:
            try:
                self._atributes_dic.pop(key)
            except KeyError:
                continue
