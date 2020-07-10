import discord
import asyncio
from discord.ext import commands

from bot_base import bot
from bot_base import songs
from bot_base import play_next_song

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=".help"))

@bot.event
async def on_message(msg):
    pass

@bot.event
async def audio_player_task():
    while True:
        play_next_song.clear()
        current = await songs.get()
        current.start()
        await play_next_song.wait()