import discord
from discord.ext import commands
from bot_commands import channels


help_command = commands.HelpCommand()

class help_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, context):

        cog = bot.get_cog()
        print([c.name for c in commands])



        '''Escribe los comandos disponibles para el usuario que mandó el mensaje'''
        embed = discord.Embed(
            title=".help", 
            description="Estos son los comandos disponibles para {.author.mention}:".format(context.message), 
            color=0x00ecff)

        embed.add_field(name=".help", value="Enseña los comandos disponibles", inline=False)
        embed.add_field(name=".ctc 'name'", value="create text channel en categoria donde se envía el mensaje", inline=False)
        if context.message.author.guild_permissions.administrator:
            embed.add_field(name=".rtc", value="remove text channel donde se envía el mensaje", inline=False)
        embed.add_field(name=".cvc 'name'", value="create voice channel en categoria donde está el usuario", inline=False)
        if context.message.author.guild_permissions.administrator:
            embed.add_field(name=".rvc", value="remove voice channel en el que está el usuario", inline=False)
        await context.message.channel.send(embed=embed)
        return

