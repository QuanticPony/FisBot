import discord
import asyncio
from discord.ext import commands
from bot_commands import channels

class FisBot(commands.Bot):
    async def __init__(self, command_prefix, help_command=_default, description=None, **options):
        super().__init__(command_prefix, help_command=help_command, description=description, **options)
        self.add_cog(channels(self))

    @bot.command(pass_context=True)
    async def extensions(self, order, extension):
        cogs = bot.cogs
        if order == 'enabled':
            for cog[0] in cogs:
                frase += cog[0] + '\n'

            await ctx.send(frase)
        
        if order == 'load':
            self.add_extension(str(extension))

        if order == 'reload':
            self.reload_extension(str(extension))

        if order == 'unload':
            self.unload_extension(str(extension))



        
        

bot = commands.Bot(command_prefix=commands.when_mentioned_or("."))

bot.remove_command('help')


#songs = asyncio.Queue()
#play_next_song = asyncio.Event()
#bot.loop.create_task(bot_events.audio_player_task())
