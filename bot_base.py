import discord
#import random
#import user_class

from discord.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned_or("."))

msg = discord.User

def is_me(msg):
    return msg.author == bot.user

def is_command(msg):
    if msg.content.startswith(".ntc"):
        return True

    return False
    

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=".help"))

@bot.event
async def on_message(msg):
    if msg.content.startswith(".help"):
        channel = msg.channel
        await channel.send(
            '''```css
Commandos disponibles:
    .help   
    .prueba
    .ntc "name" (new text channel at user's menssage category)   
    .nvc "name" (new voice channel at current user category)   
            ```''')

    if msg.content.startswith(".prueba"):
        channel = msg.channel
        await channel.send("prueba")

    if msg.content.startswith(".ntc"):
        prefix, name = msg.content.split()
        category = await msg.channel.category
        await category.create_text_channel(name=name)

    if msg.content.startswith(".nvc"):
        prefix, name = msg.content.split()
        channel = msg.author.voice.channel
        await channel.category.create_voice_channel(name=name)

    if msg.content.startswith(""):
        pass



token_file = open("token.txt", "r")
token = token_file.read()
token_file.close()
bot.run(str(token))   # TODO: leer el token del archivo token.txt