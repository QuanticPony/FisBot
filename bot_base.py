import discord
import asyncio
import bot_events
import bot_commands
from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or("."))

songs = asyncio.Queue()
play_next_song = asyncio.Event()
bot.loop.create_task(bot_events.audio_player_task())

# Token read and run bot
with open("token.txt", "r").read() as token:
    bot.run(str(token))

#token_file = open("token.txt", "r")
#token = token_file.read()
#token_file.close()
#bot.run(str(token))