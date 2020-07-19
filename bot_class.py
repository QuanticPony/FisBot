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

    def __init__(self, command_prefix: str):
        super().__init__(command_prefix=commands.when_mentioned_or("."))
        self.cog_list = ['extension_managment']
        self.load_extension('extension_managment')