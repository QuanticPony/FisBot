import discord
import asyncio
from discord.ext import commands


def context_is_admin(context):
    '''Devuelve True si el author del contexto que activa cierta funcion del Bot tiene permisos de administrador en dicho Servidor.
    Esta funcion se puede importar a otras extensiones para ponerla como check de commandos y cogs'''
    
    if context.guild:
        return context.message.author.guild_permissions.administrator
    else:
        return False


class FisBot(commands.Bot):    

    def __init__(self, command_prefix: str):
        super().__init__(command_prefix=commands.when_mentioned_or("."))
        self.extensions_list = [
            'fisbot.custom_help.loader',
            'fisbot.basics.loader',
            'fisbot.music_commands.loader',
            'fisbot.task_commands.loader',
            #'custom_roles'
            ]
        self.add_extensions(self.extensions_list)
        

    def add_extension(self, extension_name):
        '''Añade una extension al Bot. Tiene que haber un archivo con el nombre introducido y el archivo deberia contener una funcion del siguiente estilo:\n
        def setup(bot):
            bot.add_cog(commands.Cog: ClassName(bot))
            <code>
        '''
        self.load_extension(extension_name)

    def add_extensions(self, extensions_names):
        '''Añade una lista de extensiones al Bot. Tiene que haber un archivo por cada elemento de la lista con el nombre introducido y cada archivo deberia contener una funcion del siguiente estilo:\n
        def setup(bot):
            bot.add_cog(commands.Cog: ClassName1(bot))
            <code>
        '''
        for extenion_name in extensions_names:
            self.load_extension(extenion_name)

    def del_extension(self, extension_name):
        '''Quita una extension al Bot. Tiene que haber un archivo con el nombre introducido y el archivo puede contener una funcion del siguiente estilo:\n
        def teardown(bot):
            bot.remove_cog(cog_name: string)
            <code>
        '''
        self.unload_extension(extension_name)
        
    def del_extensions(self, extensions_names):
        '''Quita una lista de extensiones al Bot. Tiene que haber un archivo por cada elemento de la lista con el nombre introducido y cada archivo puede contener una funcion del siguiente estilo:\n
        def terdown(bot):
            bot.remove_cog(cog_name1: string)
            <code>
        '''
        for extenion_name in extensions_names:
            self.unload_extension(extenion_name)