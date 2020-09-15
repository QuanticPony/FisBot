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
        aliases=['nivel','lvl','karma'],
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
            await ctx.send(f"{ctx.author.mention}", embed=embed)

    @commands.group(
        pass_context=True,
        hidden=True,
        name='user',
        aliases=['usuario'],
        brief='Permite modificar la base de datos de los usuarios',

    )
    async def _users(self, ctx):

         if not ctx.invoked_subcommand:
            await self.level(ctx)

    @_users.command(
        pass_context=True,
        name='modify',
        aliases=['mod'],
        help='''''',
        description='''''',
        brief='''Modifica un usuario en la base de datos''',
        usage='.user modify',
        checks=[context_is_admin]
    )
    async def _modify(self, ctx):

        disc_user = ctx.message.mentions
        if disc_user:
            disc_user = disc_user[0]
        
        user = await FisUser.init_with_member(disc_user, context=ctx)
        await user.modify()

    @_users.command(
        pass_context=True,
        name='delete',
        aliases=['del'],
        help='''''',
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
        name='',
        aliases=['k'],
        help='''¿? ```.```
        ¿? ```.```''',
        brief='''karma de un usuario''',
        description='''''',
        usage=''
    )
    async def _karma(self, ctx):

        if not ctx.invoked_subcommand:
            await self.level(ctx)
        
    @_karma.group(
        pass_context=True,
        name='',
        aliases=['u'],
        help='''¿? ```.```
        ¿? ```.```''',
        brief='''Dar karma a alguien''',
        description='''''',
        usage=''
    )
    async def _up(self, ctx):

        if  ctx.message.mentions:
            for user in ctx.message.mentions:

                user = UsersDB.get_user(user.id)

                if not user:
                    UsersDB.add_user(user)
                
                if user.id != ctx.author.id:
                    user.karma += 1
                    UsersDB.update_user(user)
        await ctx.message.delete()
                
    @_karma.group(
        pass_context=True,
        name='down',
        aliases=['d'],
        help='''¿Quieres quitar karma a @Marcos porque es malo? ```.karma down @Marcos```
        ¿? ```.```''',
        brief='''Quitar karma a alguien''',
        description='''''',
        usage='.karma down <user/s_mention/s>'
    )
    async def _down(self, ctx):
        
        if  ctx.message.mentions:
            for user in ctx.message.mentions:

                user = UsersDB.get_user(user.id)

                if not user:
                    UsersDB.add_user(user)
                
                if user.id != ctx.author.id:
                    user.karma -= 1
                    UsersDB.update_user(user)
        await ctx.message.delete()