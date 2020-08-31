import discord
import asyncio
import fisbot
from fisbot import FisBot, FisUser, UsersDB

bot = FisBot(command_prefix='.')

BOT_PATH = '/home/pi/Bots/Fisbot/FisBot/'

with open(BOT_PATH + "token.txt", "r") as token_file:
    bot.run(str(token_file.read()))