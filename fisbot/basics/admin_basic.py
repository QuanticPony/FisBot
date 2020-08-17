import discord
import asyncio
import random
from discord.ext import commands
from ..classes.bot_class import context_is_admin

class admin_basic_commands(
    commands.Cog,
    name='Comandos basicos',
    ):
    '''Conjunto de comandos que permite la manipulación básica del bot'''
    
    def __init__(self, bot):
        self.bot = bot
        self.cog_check(context_is_admin)

    @commands.command(
        pass_context=True, 
        aliases=['estado','juego'],
        help='''¿Quiere cambiar el estado del bot a patatas? ```.status patatas```''',
        brief='''Cambia el estado del bot''',
        description='''Cambia el estado del bot. En el caso default pone como estado .help''',
        usage='.status [estado]'
    )
    async def status(self, context, game=None):
        if game == None:
            game = context.prefix + 'help'
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=game))

    @commands.command(
        pass_context=True,
        hidden=True,
        check=[context_is_admin]
    )
    async def prueba(self, ctx):
        from ..database.users import UsersDB
        from ..classes.user_class import FisUser

        bd = UsersDB()
        server = ctx.guild
        for member in server.members:
            if member.nick:
                user = FisUser(member.id, member.nick)
            else:
                user = FisUser(member.id, member.name)
            bd.update_user(user)

        await ctx.message.add_reaction("🔄")



    @commands.command(
        pass_context=True, 
        aliases=['sd', 'shut', 'apagar'],
        help='''¿Quiere apagar el bot? No lo haga si no es imprescindible, pero se hace asi: ```.shutdown```''',
        brief='''Apaga el bot''',
        description='''Apaga el bot. No lo haga si no es imprescindible''',
        usage='.shutdown'
    )
    async def shutdown(self, ctx):
        await self.bot.logout()
    
    
    @commands.command(
        pass_context=True, 
        aliases=['reset','restart', 'reiniciar'],
        help='''¿Se ha cambiado alguna libreria del bot y quiere actualizar su configuracion no imprescindible? ```.reload```
        ¿Quieres y necesitas reiniciar, pero tienes la musica activada y no te apetece volverle a pedir que reproduzca?```.restart -music```''',
        brief='''Recarga el bot''',
        description='''Recarga el bot y actualiza los comandos de todas las extensiones habilitadas''',
        usage='.reload',
        check=[context_is_admin]
        )
    async def reload(self, ctx, *arg):
        if arg:
            arg[0] = arg[0].strip('-')

        def check(arg, cog_name):
            if not arg:
                return True
            else:
                return arg[0] in cog_name

        for cog_name in self.bot.extensions_list:
            if cog_name != 'fisbot.basics.loader' and check:
                self.bot.reload_extension(cog_name)


        await ctx.message.add_reaction("🔄")
        self.bot.reload_extension('fisbot.basics.loader')
        
