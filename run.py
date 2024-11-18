import discord
import asyncio
import fisbot
from fisbot import FisBot

import logging


handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

logging.basicConfig(filename="fisbot.log", encoding="utf-8", filemode="w")

BOT_PATH =''


intents = discord.Intents.all()


with open(BOT_PATH + "owner_id.txt", "r") as owner_file:
    me_id = int(owner_file.read())

with open(BOT_PATH + "token.txt", "r") as token_file:
    token = str(token_file.read())

bot = FisBot(command_prefix='.', path=BOT_PATH, owner_id=me_id, intents=intents)



async def activate_extensions():
    await bot.activate_extensions()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(activate_extensions())

    bot.run(token, log_handler=handler, log_level=logging.DEBUG)


    