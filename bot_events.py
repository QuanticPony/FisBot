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
    if msg.content.startswith(".help"):
        embed = discord.Embed(
            title=".help", 
            description="Estos son los comandos disponibles para {.author.mention}:".format(msg), 
            color=0x00ecff)

        embed.add_field(name=".help", value="Enseña los comandos disponibles", inline=False)
        embed.add_field(name=".ctc 'name'", value="create text channel en categoria donde se envía el mensaje", inline=False)
        if msg.author.guild_permissions.administrator:
            embed.add_field(name=".rtc", value="remove text channel donde se envía el mensaje", inline=False)
        embed.add_field(name=".cvc 'name'", value="create voice channel en categoria donde está el usuario", inline=False)
        if msg.author.guild_permissions.administrator:
            embed.add_field(name=".rvc", value="remove voice channel en el que está el usuario", inline=False)
        await msg.channel.send(embed=embed)
        return

    if msg.content.startswith(".jose") and msg.author.guild_permissions.administrator:
        channel1 = msg.author.voice.channel
        print(str(channel1.type))
        channels = msg.author.voice.channel.category.channels
        for channel2 in channels:
            if channel2 != msg.author.voice.channel and str(channel2.type) == 'voice' and msg.author.id == 230323162414317568:
                await msg.author.move_to(channel2)
                await msg.author.move_to(channel1)
                await msg.delete()
                break
        return

    if msg.content.startswith(".ctc"):
        try:
            prefix, name = msg.content.split() 
        except ValueError:
            await msg.channel.send("Especifica: .ctc \"name\" ")
        category = msg.channel.category
        await category.create_text_channel(name=name)
        return

    if msg.content.startswith(".rtc") and msg.author.guild_permissions.administrator:
        def confirm(reaction, user):
            return str(reaction.emoji) == '✅' and msg.author == user
        msg_conf = await msg.channel.send("¿Está seguro de que quiere borrar {.channel.mention}?\tSi: ✅\t No: ❌".format(msg))
        await msg_conf.add_reaction("✅")
        await msg_conf.add_reaction("❌")
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=confirm)
        except asyncio.TimeoutError:
            await msg_conf.delete()
        else:
            await msg.channel.delete()
        return


    if msg.content.startswith(".cvc"):
        try:
            prefix, name = msg.content.split()
        except ValueError:
            await msg.channel.send("Especifica: .cvc \"name\" ")
        channel = msg.author.voice.channel
        await channel.category.create_voice_channel(name=name)
        return
    
    if msg.content.startswith(".rvc") and msg.author.Permissions.administrator:
        def confirm(reaction, user):
            return str(reaction.emoji) == '✅' and msg.author == user
        msg_conf = await msg.channel.send("¿Está seguro de que quiere borrar {.channel.mention}? Si: ✅   No: ❌".format(msg.author.voice))
        await msg_conf.add_reaction("✅")
        await msg_conf.add_reaction("❌")
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=confirm)
        except asyncio.TimeoutError:
            await msg_conf.delete()
        else:
            channel = msg.author.voice.channel
            await msg_conf.delete()
            await channel.delete()
        return

@bot.event
async def audio_player_task():
    while True:
        play_next_song.clear()
        current = await songs.get()
        current.start()
        await play_next_song.wait()