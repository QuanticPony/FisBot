import discord
import asyncio
from discord.ext import commands
from classes.bot_class import context_is_admin

class extensions_managment(
    commands.Cog,
    name='''Control de extensiones'''
    ):
    ''' Conjunto de comandos que permite la manipulación de las extensiones del bot'''

    def __init__(self, bot):
        self.bot = bot
        self.cog_check(context_is_admin)


    @commands.command(
        pass_context=True, 
        aliases=['ext'],
        help='''¿Ha añadido un archivo llamado hola_mundo.py a la carpeta de FisBot y quiere añadir los comandos al bot?```.extensions load hola_mundo```
        ¿Quiere recargar la extension hola_mundo porque ha actualizado los ejemplos de un comando?```.extensions reload hola_mundo```
        ¿Se ha cansado de la extension hola_mundo?```.extensions unload hola_mundo```
        ''',
        brief='''Controla las extensiones del bot. Permite habilitarlas y quitarlas''',
        description='''Permite la manipulación de las extensiones del bot. Las diferentes ordenes son:
        \nenabled: Muestra las extensiones habilitada
        \nload:    Carga la extensión [extension]
        \nreload:  Recarga la extensión [extension]
        \nunload:  Descarga la extensión [extension]''',
        usage='.extensions <enabled|load|reload|unload> [extension]'
    )
    async def extensions(self, ctx, order, *extension):
        if order == 'enabled':
            enabled_extensions = '```\n'

            for cog_name in self.bot.extensions_list:
                enabled_extensions += cog_name + '\n'
            else:
                enabled_extensions += '```'

            if enabled_extensions != '':
                await ctx.send(enabled_extensions)
        
        if order == 'load':
            self.bot.extensions_list.append(extension[0])
            self.bot.load_extension(extension[0])
            await ctx.message.add_reaction("✅")
        
        if order == 'reload':
            self.bot.reload_extension(extension[0])
            await ctx.message.add_reaction("🔄")
        
        if order == 'unload' and extension != 'basics.loader':
            self.bot.extensions_list.remove(extension[0])
            self.bot.unload_extension(extension[0])
            await ctx.message.add_reaction("✅")
