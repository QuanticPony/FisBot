import discord
#import random
#import user_class

from discord.ext import commands

#bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'), help_command=".Help")
#client = discord.Client()
bot = commands.Bot(command_prefix=commands.when_mentioned_or("."))

@bot.event
async def on_ready():
    print("Listo jefe!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=".Prueba"))


@bot.event
async def on_message(msg_in):
    if msg_in.content.startswith(".Prueba"):
        channel = msg_in.channel
        await channel.send("Prueba")

    if msg_in.content.startswith(".Prueba2"):
        channel = msg_in.channel
        await channel.send("Prueba2")



## Para debug
#import logging
#logging.basicConfig(level=logging.INFO)
#
#
#    dictionary = {}
#    user_names = open("user_names.txt","r")
#    line = user_names.readline()
#    while line:
#        line = line.split(" ",2)
#        user_id = int(line[0])
#        user_index = int(line[1])   #TODO: debug esa parte
#        dictionary.setdefault(user_id, user_index)
#
#        line = user_names.readline()
#    user_names.close
#
#
#    user_dat = open("user_dat.dat","r+")
#    user_dat.se
#    user_dat.close
#
#
#
#
#    from discord.ext import commands
#    descripcion = '''Bot en proceso de mejora, tratar con cuidado'''
#    bot = commands.Bot(command_prefix=commands.when_mentioned_or('.'), description=descripcion)
#    bot.game(".Help")
#
#    msg = discord.Message
#    msg.channel = 0
#
#    @bot.event
#    async def on_ready():
#        print('{0.user} ha llegado!!'.format(bot))
#
#    @bot.event
#    async def on_message(message):
#        if message.author == bot.user:
#            return
#
#        if message.content == ".Prueba":
#            msg.c

        


token_file = open("token.txt", "r")
token = token_file.read()
token_file.close()
bot.run(str(token))   # TODO: leer el token del archivo token.txt