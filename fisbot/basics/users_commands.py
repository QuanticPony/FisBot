import discord
from discord.ext import commands
from ..classes.bot_class import context_is_admin
from ..classes.user_class import FisUser
from ..database.users import UsersDB

class users_cog(
    commands.Cog,
    name='Usuarios'
    ):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        pass_context=True, 
        aliases=['nivel','lvl'],
        help='''¿Quiere ver tu nivel? ```.level```
        ¿Quieres ver el nivel de <@730713148977578024>? ```.level @FisBot```''',
        brief='''Muestra nivel y experiencia''',
        description='''Muestra el nivel y la experiencia del autor del mensaje.
        En el caso de mencionar a alguien muestra su informacion''',
        usage='.level [member|s]'
    )
    async def level(self, ctx):

        embeds_list = []
        if not ctx.message.mentions:

            user = UsersDB.get_user(ctx.author.id)

            if not user:
                UsersDB.add_user(user)
            await user.init_display(ctx)
            embeds_list.append(await user.embed_show())

        else:
            for user in ctx.message.mentions:

                user = UsersDB.get_user(user.id)

                if not user:
                    UsersDB.add_user(user)
                await user.init_display(ctx)
                embeds_list.append(await user.embed_show())

            await ctx.message.delete()

        for embed in embeds_list:
            await ctx.send(embed=embed)


    @commands.group(
        pass_context=True,
        hidden=True,
        name='user',
        aliases=['usuario'],
        brief='Permite modificar la base de datos de los usuarios',
        description='''Permite acceder a los comandos de modificacion y eliminacion de usuarios en la base de datos.
        Los subcomandos disponibles son:
        ```
        modify: <ADMIN> Modifica un usuario
        delete: <ADMIN> Elimina un usuario
        ```''',
        usage='.user <subcommand> <user_mention>',
        checks=[context_is_admin]
    )
    async def _user(self, ctx):
        pass


    @_user.command(
        pass_context=True,
        name='modify',
        aliases=['mod'],
        help='''¿Quieres modificar los atributos de @Jose?```.user modify @Jose```''',
        description='''Permite modificar nivel, experiencia, karma, y nombre de un usuario. Evidentemente si eres administrador''',
        brief='''Modifica un usuario en la base de datos''',
        usage='.user modify <user_mention>',
        checks=[context_is_admin]
    )
    async def _modify(self, ctx):

        disc_user = ctx.message.mentions
        if disc_user:
            disc_user = disc_user[0]
        
        user = await FisUser.init_with_member(disc_user, context=ctx)
        await ctx.message.delete()
        await user.modify()


    @_user.command(
        pass_context=True,
        name='delete',
        aliases=['del'],
        help='''¿Quiers borrar a @Pablo porque se ha ido del servidor? ```.user delete @Pablo```''',
        description='''**No usar este comando sin permiso previo** \nElimina al usuario mencionado de la base de datos''',
        brief='''Elimina un usuario de la base de datos''',
        usage='.user delete <user_mention>',
        checks=[context_is_admin]
    )
    async def _delete(self, ctx):

        disc_user = ctx.message.mentions
        if disc_user:
            disc_user = disc_user[0]
        
        user = await FisUser.init_with_member(disc_user, context=ctx)
        await ctx.message.delete()
        await user.delete()


    @commands.group(
        pass_context=True,
        name='karma',
        aliases=['k'],
        help='''¿Quieres ver tu karma? ```.karma```
        ¿Quieres ver el karma de @Victor? ```.karma @Victor```''',
        brief='''Karma de un usuario''',
        description='''Te muestra la informacion del usuario, igual que el comando ```.level```''',
        usage='.karma [user/s_mention/s]'
    )
    async def _karma(self, ctx):

        await ctx.send('**Uso:** Para dar karma a alguien solo tienes que reaccionar con ⬆️ en un mensaje suyo. Para quitar ⬇️')
        if not ctx.invoked_subcommand:
            await self.level(ctx)