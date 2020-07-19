import discord
import asyncio
from discord.ext import commands


class extensions_managment(commands.Cog):
    '''Conjunto de comandos que permite la manipulación de las extensiones del bot'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True, 
        aliases=['ext'],
        help='''Permite la manipulación de las extensiones del bot. Las diferentes ordenes son:
        \nenabled\t\t\t Muestra las extensiones habilitada
        \nload\t[extensión]\t Carga la extensión [extensión]
        \nreload\t[extensión]\t Recarga la extensión [extensión]
        \nunload\t[extensión]\t Descarga la extensión [extensión]
        ''',
        brief='''[Admin required]''',
        description='''COMANDO .extensions'''
    )
    async def extensions(self, ctx, order, *extension):
        if ctx.message.author.guild_permissions.administrator == False:
            await ctx.message.add_reaction("❌")
            return
        #print(orden)
        #print(str(extension[0]))

        if order == 'enabled':
            enabled_extensions = '```\n'

            for cog_name in self.bot.cog_list:
                enabled_extensions += cog_name + '\n'
            else:
                enabled_extensions += '```'

            if enabled_extensions != '':
                await ctx.send(enabled_extensions)
        
        if order == 'load':
            self.bot.cog_list.append(extension[0])
            self.bot.load_extension(extension[0])
            await ctx.message.add_reaction("✅")
        
        if order == 'reload':
            self.bot.reload_extension(extension[0])
            await ctx.message.add_reaction("🔄")
        
        if order == 'unload' and extension != 'extension_managment':
            self.bot.cog_list.remove(extension[0])
            self.bot.unload_extension(extension[0])
            await ctx.message.add_reaction("❌")


def setup(bot):
    bot.add_cog(extensions_managment(bot))
