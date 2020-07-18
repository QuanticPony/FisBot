import discord
import asyncio
from discord.ext import commands



class extensions_managment(commands.Cog):
    '''[Admin required] Conjunto de comandos que permite la manipulación de las extensiones del bot'''
    def __init__(self, bot):
        self.bot = bot


    @commands.command(pass_context=True)
    async def reload(self, ctx):
        '''Recarga el bot y actualiza los comandos'''
        if ctx.message.author.guild_permissions.administrator == False:
             return
        self.bot.reload_extension('extension_managment')
        await ctx.message.add_reaction("✅")


    @commands.command(pass_context=True)
    async def extensions(self, ctx, order, *extension):
        '''<enabled/load/reload/unload> <file_name>'''

        if ctx.message.author.guild_permissions.administrator == False:
             return
        #print(orden)
        #print(str(extension[0]))

        cogs = self.bot.cogs
        print(format(cogs))

        if order == 'enabled':
            frase = ''
            print(str(cog) for cog in cogs)
        
            if frase != '':
                await ctx.send(frase)
        
        if order == 'load':
            await self.bot.load_extension(extension[0])
        
        if order == 'reload':
            await self.bot.reload_extension(extension[0])
        
        if order == 'unload' and extension != 'extension_managment.':
            await self.bot.unload_extension(extension[0])


def setup(bot):
    bot.add_cog(extensions_managment(bot))
