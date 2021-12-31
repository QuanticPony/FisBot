import discord
import asyncio
import fisbot
from fisbot import FisBot
from fisbot.classes.bot_class import FisBot_reminder

BOT_PATH =''

intents = discord.Intents.all()

with open(BOT_PATH + "owner_id.txt", "r") as owner_file:
    id = int(owner_file.read())

bot = FisBot_reminder(path=BOT_PATH, owner_id=id, intents=intents)

with open(BOT_PATH + "token.txt", "r") as token_file:
    bot.run(str(token_file.read()))