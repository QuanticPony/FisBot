import discord
import asyncio
from bot_class import FisBot

bot = FisBot(command_prefix='.')

with open("token.txt", "r") as token_file:
    bot.run(str(token_file.read()))