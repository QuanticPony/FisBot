import discord
import asyncio
from discord.ext import commands


class extensions_managment(commands.Cog):
    '''[Admin required] Conjunto de comandos que permite la manipulación de las extensiones del bot'''
    def __init__(self, bot):
        self.bot = bot
        self.cogs = []
        self.cogs.append('extensions_managment')


    @commands.command(pass_context=True, aliases=['sd'])
    async def shutdown(self, ctx):
        await self.bot.logout()

    @commands.command(pass_context=True, aliases=['restart'])
    async def reload(self, ctx):
        '''Recarga el bot y actualiza los comandos'''
        if ctx.message.author.guild_permissions.administrator == False:
             return
        for cog_name in self.cogs:
                self.bot.reload_extension(cog_name)
        self.bot.reload_extension('extension_managment')
        await ctx.message.add_reaction("🔄")


    @commands.command(pass_context=True, aliases=['ext'])
    async def extensions(self, ctx, order, *extension):
        '''<enabled/load/reload/unload> [file_name]'''

        if ctx.message.author.guild_permissions.administrator == False:
             return
        #print(orden)
        #print(str(extension[0]))

        if order == 'enabled':
            enabled_extensions = '```\n'

            for cog_name in self.cogs:
                enabled_extensions += cog_name + '\n'
            else:
                enabled_extensions += '```'

            if enabled_extensions != '':
                await ctx.send(enabled_extensions)
        
        if order == 'load':
            self.cogs.append(extension[0])
            self.bot.load_extension(extension[0])
            await ctx.message.add_reaction("✅")
        
        if order == 'reload':
            self.bot.reload_extension(extension[0])
            await ctx.message.add_reaction("🔄")
        
        if order == 'unload' and extension != 'extension_managment.':
            self.cogs.remove(extension[0])
            self.bot.unload_extension(extension[0])
            await ctx.message.add_reaction("❌")


def setup(bot):
    bot.add_cog(extensions_managment(bot))
