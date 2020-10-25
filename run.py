import discord
import asyncio
import fisbot
from fisbot import FisBot, FisUser, UsersDB

BOT_PATH =''#'/home/pi/Bots/Fisbot/FisBot/'

bot = FisBot(command_prefix='-', path=BOT_PATH)

with open(BOT_PATH + "token.txt", "r") as token_file:
    bot.run(str(token_file.read()))