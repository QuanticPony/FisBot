import discord
import asyncio
import fisbot
from fisbot import FisBot

BOT_PATH =''

intents = discord.Intents.all()

with open(BOT_PATH + "owner_id.txt", "r") as owner_file:
    id = int(owner_file.read())

bot = FisBot(command_prefix='.', path=BOT_PATH, owner_id=id, intents=intents)

with open(BOT_PATH + "token.txt", "r") as token_file:
    bot.run(str(token_file.read()))