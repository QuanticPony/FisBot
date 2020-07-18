import discord
import asyncio
from discord.ext import commands
from bot_commands import channels


class FisBot(commands.Bot):
    async def __init_status__(self):
        await self.change_presence(status=discord.Status.idle, activity=self.game)

    def __init__(self, command_prefix: str):
        super().__init__(command_prefix=commands.when_mentioned_or("."))
        game = discord.Game(".help")
        self.load_extension('extension_managment')
        self.__init_status__

  