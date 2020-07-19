import discord
import asyncio
from discord.ext import commands

class basic_commands(commands.Cog, command_attrs=dict(hidden=False)):
    '''[Admin required] Conjunto de comandos que permite la manipulación básica del bot'''

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        pass_context=True, 
        aliases=['sd', 'shut', 'apagar', 'stop'],
        help='''Apaga el bot,''',
        brief='''[Admin required]''',
        description='''COMANDO .shutdown'''
    )
    async def shutdown(self, ctx):
        await self.bot.logout()
    
    @commands.command(
        pass_context=True, 
        aliases=['restart', 'reiniciar'],
        help='''Recarga el bot y actualiza los comandos de todas las extensiones habilitadas''',
        brief='''[Admin required]''',
        description='''COMANDO .reload'''
        )
    async def reload(self, ctx):
        if ctx.message.author.guild_permissions.administrator == False:
             return
        for cog_name in self.bot.cog_list:
            if cog_name != 'extension_managment':
                self.bot.reload_extension(cog_name)
        await ctx.message.add_reaction("🔄")
        self.bot.reload_extension('extension_managment')

def setup(bot):
    bot.add_cog(basic_commands(bot))
