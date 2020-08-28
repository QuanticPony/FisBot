import discord
import asyncio
import random
from discord.ext import commands
from ..classes.bot_class import context_is_admin

class cog_managment(
    commands.Cog,
    name='''Control de comandos'''
    ):
    '''Conjunto de comandos que permite la manipulacion de los conjuntos de commandos del bot'''

    def __init__(self, bot):
        self.bot = bot
        self.cog_check(context_is_admin)

    @commands.group(
        pass_context=True, 
        help='''
        Permite cargar, descargar las categorias de comandos de manera independiente de las extensiones a las que pertenezcan.
        Si no se invoca un subcomando escribe una lista con las categorias habilitadas.
        ''',
        brief='''Opera conjuntos de comandos''',
        description='''COMANDO .cog''',
        usage='.cog <subcommand>'
    )
    async def cog(self, context):
        if context.invoked_subcommand is None:
            message = '```\n'
            for key in self.bot.cogs.keys():
                message += key + '\n' 
            else:
                message += '```'
            await context.send(message)
    

    @cog.command(
        pass_context=True, 
        help='''
        Permite cargar categorias de comandos
        ''',
        brief='''Permite cargar categorias de comandos''',
        description='''COMANDO .cog add''',
        usage='.cog add <cog_name>'
    )
    async def add(self, context, *cog_name):
        if cog_name is None:
            await context.send('Invalid Syntax: cog add <cog_name>')
        else:
            requested_cog = self.bot.get_cog(cog_name)
            if requested_cog:
                self.bot.add_cog(requested_cog(self.bot))
            else:
                context.send('No se encontro la categoria de commandos {0}'.format(cog_name))

    @cog.command(
        pass_context=True,
        help='''
        Permite cargar categorias de comandos
        ''',
        aliases=['del'],
        brief='''Permite descargar categorias de comandos''',
        description='''COMANDO .cog remove''',
        usage='.cog remove <cog_name>'
    )
    async def remove(self, context, cog_name):
        if cog_name in self.bot.cogs:
            self.bot.remove_cog(cog_name)
        else:
            await context.send('No existe la categoria de comandos '+ cog_name + ', o no esta cargada')
