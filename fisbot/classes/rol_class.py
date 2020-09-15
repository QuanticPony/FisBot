import discord
from discord.ext import commands
import asyncio
from random import randint
from .display_class import *

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

    def __init__(self, rol_id=0, level=0, description='None', privileges='None', context=None, name='None'):
        super().__init__(context=context)
        self.id = rol_id
        self.name = name
        self.level = level
        self.description = description
        self.privileges = privileges

        from ..database.roles import RolesDB
        self.database = RolesDB

        if context:
            self.init_display(context)


    @classmethod
    async def init_and_discord(cls, ctx: commands.Context):
        '''Inicia la clase `FisRol` y el objeto de discord `Role` asociado. Y te permite modificarlos por privado '''

        instance = cls(context=ctx)

        instance.name = 'None'
        new_role = await instance.create_discord_obj(instance.name)
        instance.id = new_role.id
        instance._disc_obj = new_role

        await instance.create()
        return instance

    @classmethod
    def init_from_discord(cls, ctx: commands.Context, role: discord.Role):
        '''Inicia la clase `FisRol` a partir de un `discord.Role`. Mira en la base de datos a ver si encuentra un rol
        con la misma id. Si no lo encuentra devuelve `None`'''

        instance = cls().database.get_rol_id(role.id)
        instance.init_display(ctx)
        instance._disc_obj = role
        return instance

# Funciones de la clase FisRol

    def check_new_rol_needed(self, user):
        '''Devuelve el rol `FisRol` que deberia tener el usuario especificado. Si no hay un rol para ese nivel devuelve `None`'''

        return self.database.get_rol(user.level)

    def prev_role_of_level(self, level: int):
        '''Devuelve el ultimo rol `FisRol` que consiguio el usuario. Devuelve `None` si no ha conseguido nunca un rol'''


        for i in reversed(range(1, level)):
            rol = self.database.get_rol(i)
            if rol: 
                if self._ctx:
                    return rol.init_display(self._ctx)
                else:
                    return rol
        else:
            return None

    async def give_to(self, user, *, guild=None) -> bool:
        '''Da al usuario especificado este rol. Se puede especificar el servidor con la palabra clave `guild`'''

        if not guild:
            try:
                guild = self._ctx.guild
            except:
                return False

        disc_user = guild.get_member(user.id)
        disc_rol = guild.get_role(self.id)
        if disc_user and disc_rol:
            await disc_user.add_roles(disc_rol)
            return True
        else:
            return False

    async def remove_from(self, user, *, guild=None) -> bool:
        '''Elimina del usuario `user` el rol. Devuelve `true`si lo consigue y `false` si no.
        Se puede especificar el servidor con la palabra clave `guild`'''

        if not guild:
            try:
                guild = self._ctx.guild
            except:
                return False
        
        disc_user = guild.get_member(user.id)
        disc_rol = guild.get_role(self.id)
        if disc_user and disc_rol:
            await disc_user.remove_roles(disc_rol)
            return True
        else:
            return False

    @check_if_context()
    async def next_rol(self, user):
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

    @check_if_context()
    async def create_discord_obj(self, role_name) -> discord.Role:
        '''Crea un rol de discord a partir de un nombre y devuelve el `discord.Role`'''

        role = await self._ctx.guild.create_role(
            hoist=False, mentionable=True, name=role_name, 
            permissions=discord.Permissions.none(),
            colour=discord.Color.from_rgb(randint(0,255),randint(0,255),randint(0,255))
            )
        return role

# Funciones sobreescritas de la clase Display

    @check_if_discord_obj()
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

    @check_if_context()
    async def discord_obj(self) -> discord.Role:

        self._disc_obj = self._ctx.guild.get_role(self.id)

        if not self._disc_obj:
            self.create_discord_obj(self._ctx)

        self.name = self._disc_obj.name
        return self._disc_obj

    @check_if_context()
    async def update_discord_obj(self) -> bool:

        try:
            await self._disc_obj.edit(name=self.name, mentionable=True)
            return True
        except:
            return False

    @check_if_discord_obj()
    def save_in_database(self) -> bool:

        self.database.add_rol(self)
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
