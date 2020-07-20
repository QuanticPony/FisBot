import discord
import asyncio
from discord.ext import commands
from bot_commands import channels

ID_ALBITA = 592426257170432001

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

    def context_is_admin(self, context):
        return context.message.author.guild_permissions.administrator

    def __init__(self, command_prefix: str):
        super().__init__(command_prefix=commands.when_mentioned_or("."))
        self.extensions_list = [
            'cogs'
            ]
        for cog in self.extensions_list:
            self.load_extension(cog)
        