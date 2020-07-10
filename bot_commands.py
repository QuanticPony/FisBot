import discord
import asyncio
import bot_events
from discord.ext import commands

from bot_base import bot
from bot_base import songs
from bot_base import play_next_song

def toggle_next():
    bot.loop.call_soon_threadsafe(play_next_song.set)


@bot.command(pass_context=True)
async def play(ctx, url):
    if not bot.is_voice_connected(ctx.message.server):
        voice = await bot.join_voice_channel(ctx.message.author.voice_channel)
    else:
        voice = bot.voice_bot_in(ctx.message.server)

    player = await voice.create_ytdl_player(url, after=toggle_next)
    await songs.put(player)


@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(
        title=".help", 
        description="Estos son los comandos disponibles para {.author.mention}:".format(ctx.message), 
        color=0x00ecff)

    embed.add_field(name=".help", value="Enseña los comandos disponibles", inline=False)
    embed.add_field(name=".ctc 'name'", value="create text channel en categoria donde se envía el mensaje", inline=False)
    if ctx.message.author.guild_permissions.administrator:
        embed.add_field(name=".rtc", value="remove text channel donde se envía el mensaje", inline=False)
    embed.add_field(name=".cvc 'name'", value="create voice channel en categoria donde está el usuario", inline=False)
    if ctx.message.author.guild_permissions.administrator:
        embed.add_field(name=".rvc", value="remove voice channel en el que está el usuario", inline=False)
    await ctx.message.channel.send(embed=embed)
    return



@bot.commands(pass_context=True)
async def ctc(msg):
    try:
        prefix, name = msg.content.split() 
    except ValueError:
        await msg.channel.send("Especifica: .ctc \"name\" ")
    category = msg.channel.category
    await category.create_text_channel(name=name)


@bot.command(pass_context=True)
async def join(ctx):
    "El bot entra en el canal de voz"
    await ctx.message.author.voice.channel.connect()

@bot.command(pass_context=True)
async def leave(ctx):
    "El bot sale del canal de voz"
    voice_client = bot.voice_client_in(ctx.message.server)
    await voice_client.disconnect()
