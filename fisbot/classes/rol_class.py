import discord
import asyncio
from random import randint
from .user_class import FisUser
from .class_modifier import modify

class FisRol():

    def __init__(self, rol_id=0, level=0, description='None', privileges='None'):
        self.id = rol_id
        self.level = level
        self.description = description
        self.privileges = privileges
        from ..database.roles import RolesDB
        self.database = RolesDB()


    def discord_rol(self, ctx) -> discord.Role:
        '''Devuelve el rol de discord equivalente. Si no hay devuelve `None`'''

        return ctx.guild.get_role(self.id)


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



    async def remove_from(self, ctx, user: FisUser) -> bool:
        '''Elimina del usuario `user` el rol. Devuelve `true`si lo consigue y `false` si no'''
        
        disc_user = ctx.guild.get_member(user.id)
        disc_rol = ctx.guild.get_role(self.id)
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



    async def next_rol(self, ctx, user: FisUser):
        '''Da al usuario su siguiente rol si es necesario'''

        disc_user = ctx.guild.get_member(user.id)
        disc_rol = ctx.guild.get_role(self.new_rol(user))
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


    async def create_discord_role(self, ctx, role_name) -> discord.Role:
        '''Crea un rol de discord a partir de un nombre y devuelve el `discord.Role`'''

        role = await ctx.guild.create_role(
            hoist=True, mentionable=True, name=role_name, 
            permissions=discord.Permissions.general(),
            colour=discord.Color.from_rgb(randint(0,255),randint(0,255),randint(0,255))
            )
        return role


    def _new_title(self, ctx) -> str:

        return 'Creacion de rol personalizado:'

    def _new_desc(self, ctx) -> str:

        return '''Abajo tienes la lista de todos los campos modificables. 
    Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
    *Cuando hayas acabado* presiona el boton de guardar'''



    def _mod_title(self, ctx) -> str:

        return f"Modificar **Role** id= {self.id}"


    def _mod_desc(self, ctx) -> str:

        return '''Abajo tienes la lista de todos los campos modificables. 
    Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
    *Cuando hayas acabado* presiona el boton de guardar'''


    async def modify(self, ctx) -> bool:
        '''Esta funcion permite modificar un rol a traves de una sencilla interfaz en el propio discord'''

        return await modify(self, ctx, role=True)


    async def modifyy(self, ctx):
        '''Esta funcion permite modificar un rol a traves de una sencilla interfaz en el propio discord'''

        atributes_dic = self.__dict__.copy()
        disc_rol = ctx.guild.get_role(self.id)

        channel = ctx.author.dm_channel
        if not channel:
            channel = await ctx.author.create_dm()


        embed = discord.Embed(
            title=f"Modificar: {disc_rol.mention}",
            description='Selecciona el campo a modificar:',
            color=discord.Color.dark_green()
        )
        atributes_dic.pop('id')
        atributes_dic.pop('database')

        codepoint_start = 127462  # Letra A en unicode en emoji
        things_list = {f"{chr(i)}": v for i, v in enumerate(atributes_dic, start=codepoint_start)}

        for atrib in things_list:
            embed.add_field(
                name=f"{atrib} - {things_list[atrib]}:" ,
                value=self.__dict__[things_list[atrib]],
                inline=False
                )

        message = await channel.send(embed=embed)
        for i in range(len(things_list)):
            await message.add_reaction(chr(i+codepoint_start)) 
        await message.add_reaction("💾")

        def confirm_reaction(reaction, user):
            return user.id == ctx.message.author.id
        def confirm_message(response_msg):
            return response_msg.author.id == ctx.message.author.id

        async def ask_field() -> bool:
            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=15.0, check=confirm_reaction)
                if str(reaction.emoji) == '💾':
                    return False
                
            except asyncio.TimeoutError:
                await channel.send('Se acabo el tiempo...')
                return False
            
            ask_message = await channel.send(f"Introduce un nuev@ {things_list[reaction.emoji]}:")

            try:
                response_msg = await ctx.bot.wait_for('message', timeout=60.0, check=confirm_message)
            except asyncio.TimeoutError:
                await channel.send('Se acabo el tiempo...')
                return False
              
            setattr(self, things_list[reaction.emoji], response_msg.content)
            await ask_message.delete()
            await response_msg.add_reaction("✅")

            embed.clear_fields()
            for atrib in things_list:
                embed.add_field(
                    name=f"{atrib} - {things_list[atrib]}:" ,
                    value=self.__dict__[things_list[atrib]],
                    inline=False
                    )
            await message.edit(embed=embed)
            return True


        while await ask_field():
            pass
        self.database.update_rol(self)