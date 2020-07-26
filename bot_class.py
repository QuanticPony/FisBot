import discord
import asyncio
from discord.ext import commands

ID_ALBITA = 592426257170432001


def context_is_admin(context):
    '''Devuelve True si el author del contexto que activa cierta funcion del Bot tiene permisos de administrador en dicho Servidor.
    Esta funcion se puede importar a otras extensiones para ponerla como check de commandos y cogs'''
    return context.message.author.guild_permissions.administrator


class FisBot(commands.Bot):    
    #@client.event
    #async def on_ready(self):
    #    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=".help"))
    #
    #@client.event
    #async def on_message(self, msg):
    #    if msg.author.id == ID_ALBITA:
    #        msg.add_reaction("❤️")
    #    pass

    def __init__(self, command_prefix: str):
        super().__init__(command_prefix=commands.when_mentioned_or("."))
        self.extensions_list = [
            'default_cogs',
            'music'
            ]
        self.add_extensions(self.extensions_list)

        
    def add_extension(self, extension_name):
        '''Añade una extension al Bot. Tiene que haber un archivo con el nombre introducido y el archivo deberia contener una funcion del siguiente estilo:\n
        def setup(bot):\n
        \t bot.add_cog(commands.Cog: ClassName(bot))
        \t <code>
        '''
        self.load_extension(extension_name)

    def add_extensions(self, extensions_names):
        '''Añade una lista de extensiones al Bot. Tiene que haber un archivo por cada elemento de la lista con el nombre introducido y cada archivo deberia contener una funcion del siguiente estilo:\n
        def setup(bot):\n
        \t bot.add_cog(commands.Cog: ClassName1(bot))
        \t <code>
        '''
        for extenion_name in extensions_names:
            self.load_extension(extenion_name)

    def del_extension(self, extension_name):
        '''Quita una extension al Bot. Tiene que haber un archivo con el nombre introducido y el archivo puede contener una funcion del siguiente estilo:\n
        def teardown(bot):\n
        \t <code>
        '''
        self.unload_extension(extension_name)
        
    def del_extensions(self, extensions_names):
        '''Quita una lista de extensiones al Bot. Tiene que haber un archivo por cada elemento de la lista con el nombre introducido y cada archivo puede contener una funcion del siguiente estilo:\n
        def terdown(bot):\n
        \t <code>
        '''
        for extenion_name in extensions_names:
            self.unload_extension(extenion_name)