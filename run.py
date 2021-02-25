import discord
import asyncio
import fisbot
from fisbot import FisBot

BOT_PATH ='/home/pi/Bots/Fisbot/FisBot/'

intents = discord.Intents.all()

bot = FisBot(command_prefix='.', path=BOT_PATH, intents=intents)

with open(BOT_PATH + "token.txt", "r") as token_file:
    bot.run(str(token_file.read()))