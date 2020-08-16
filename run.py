import discord
import asyncio
import fisbot
from fisbot import FisBot, FisUser
from fisbot import UsersDB

bot = FisBot(command_prefix='.')

with open("token.txt", "r") as token_file:
    bot.run(str(token_file.read()))