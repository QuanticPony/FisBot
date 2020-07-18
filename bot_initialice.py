import discord
import asyncio
from bot_class import FisBot
from user_class import FisUser

bot = FisBot(command_prefix='.')

# Token read and run bot
with open("token.txt", "r") as token_file:
    bot.run(str(token_file.read()))