import discord
import asyncio
from .user_class import FisUser

class FisRol():

    def __init__(self, rol_id=0, level=0, description='None', privileges='None'):
        self.rol_id = rol_id
        self.level = level
        self.description = description
        self.privileges = privileges
        from ..database.roles import RolesDB
        self.database = RolesDB()


    def new_rol(self, user: FisUser):
        return self.database.get_rol(user.level)

    async def modify(self, ctx):
        '''Esta funcion permite modificar un rol a traves de una sencilla interfaz en el propio discord'''

        atributes_dic = self.__dict__.copy()
        disc_rol = ctx.guild.get_role(self.rol_id)

        if not ctx.author.dm_channel:
            channel = await ctx.author.create_dm()
        else: 
            channel = ctx.author.dm_channel

        embed = discord.Embed(
            title=f"Modificar: {disc_rol.mention}",
            description='Selecciona el campo a modificar:',
            color=discord.Color.dark_green()
        )
        atributes_dic.pop('rol_id')
        atributes_dic.pop('database')

        codepoint_start = 127462  # Letra A en unicode en emoji
        things_list = {f"{chr(i)}": v for i, v in enumerate(atributes_dic, start=codepoint_start)}

        for atrib in things_list:
            embed.add_field(
                name=f"{atrib} - {things_list[atrib]}:" ,
                value=atributes_dic[things_list[atrib]],
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
            
            ask_message = await channel.send(f"Introduce un nuevo {things_list[reaction.emoji]}:")

            try:
                response_msg = await ctx.bot.wait_for('message', timeout=60.0, check=confirm_message)
            except asyncio.TimeoutError:
                await channel.send('Se acabo el tiempo...')
                return False
              
            setattr(self, things_list[reaction.emoji], response_msg.content)
            await response_msg.add_reaction("✅")
            return True


        while await ask_field():
            pass
        self.database.update_rol(self)
        return