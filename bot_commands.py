import discord
import asyncio
import bot_events
from discord.ext import commands

from bot_class import bot
from bot_class import songs
from bot_class import play_next_song

ID_JOSE = 230323162414317568

def toggle_next():
    bot.loop.call_soon_threadsafe(play_next_song.set)

@bot.command(pass_context=True)
async def help(ctx):
    '''Escribe los comandos disponibles para el usuario que mandó el mensaje'''
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

@bot.command()
async def jose(ctx):
    '''Cambia a Jose de canal de voz y lo vuelve a poner donde estaba'''
    channel1 = ctx.message.author.voice.channel
    print(str(channel1.type))
    channels = ctx.message.author.voice.channel.category.channels
    for channel2 in channels:
        if channel2 != ctx.message.author.voice.channel and str(channel2.type) == 'voice' and ctx.message.author.id == ID_JOSE:
            await ctx.message.author.move_to(channel2)
            await ctx.message.author.move_to(channel1)
            await ctx.message.delete()
            break
    return

@bot.command(pass_context=True)
async def play(ctx, url):
    if not bot.is_voice_connected(ctx.message.server):
        voice = await bot.join_voice_channel(ctx.message.author.voice_channel)
    else:
        voice = bot.voice_bot_in(ctx.message.server)

    player = await voice.create_ytdl_player(url, after=toggle_next)
    await songs.put(player)

@bot.command(pass_context=True)
async def join(ctx):
    '''El bot entra en el canal de voz'''
    await ctx.message.author.voice.channel.connect()

@bot.command(pass_context=True)
async def leave(ctx):
    '''El bot sale del canal de voz'''
    voice_client = bot.voice_client_in(ctx.message.server)
    await voice_client.disconnect()

@bot.command(pass_context=True)
async def ctc(ctx):
    '''Crea canal de texto en la categoría donde se envió el mensaje con el nombre especificado'''
    try:
        prefix, name = ctx.message.content.split() 
    except ValueError:
        await ctx.message.channel.send("Especifica: .ctc \"name\" ")
    else:
        category = ctx.message.channel.category
        await category.create_text_channel(name=name)
    return

@bot.command(pass_context=True)
async def rtc(ctx):
    '''Borra el canal de texto donde se envió el mensaje'''
    if ctx.message.author.guild_permissions.administrator:
        def confirm(reaction, user):
            return str(reaction.emoji) == '✅' and ctx.message.author == user
        msg_conf = await ctx.message.channel.send("¿Está seguro de que quiere borrar {.channel.mention}?\tSi: ✅\t No: ❌".format(ctx.message))
        await msg_conf.add_reaction("✅")
        await msg_conf.add_reaction("❌")
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=confirm)
        except asyncio.TimeoutError:
            await msg_conf.delete()
        else:
            await ctx.message.channel.delete()
        return

@bot.command(pass_context=True)
async def cvc(ctx):
    '''Crea canal de voz en la categoría donde se encuentra el autor del mensaje con el nombre especificado'''
    try:
        prefix, name = ctx.message.content.split()
    except ValueError:
        await ctx.message.channel.send("Especifica: .cvc \"name\" ")
    else:
        channel = ctx.message.author.voice.channel
        await channel.category.create_voice_channel(name=name)
    return

@bot.command(pass_context=True)
async def rvc(ctx):
    '''Elimina el canal de voz en el que se encuentra el usuario al enviar el mensaje'''
    if ctx.message.author.Permissions.administrator:
        def confirm(reaction, user):
            return str(reaction.emoji) == '✅' and ctx.message.author == user
        msg_conf = await ctx.message.channel.send("¿Está seguro de que quiere borrar {.channel.mention}? Si: ✅   No: ❌".format(ctx.message.author.voice))
        await msg_conf.add_reaction("✅")
        await msg_conf.add_reaction("❌")
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=10.0, check=confirm)
        except asyncio.TimeoutError:
            await msg_conf.delete()
        else:
            channel = ctx.message.author.voice.channel
            await msg_conf.delete()
            await channel.delete()
        return