import discord
import asyncio
from discord.ext import commands


super
class FisUser(discord.User):
    pass
    def __init__(self, *, state, data):
        self.karma = 0
        self.xp = 0
        self.level = 0
        super().__init__(*, state, data)
        return
    

    def addkarma(self):
        self.karma += 1
        return
    
    def xp_to_lvl_up(self) -> int:
        return self.xp * 10

    def addlevel(self):
        self.level += 1
        return
    
    def setlevel(self, lvl):
        self.level = lvl
        return
    
    def setkarma(self, krm):
        self.karma = krm
        return
    
    def addxp(self, amount):
        newxp = self.xp + amount
        xp_required = xp_to_lvl_up(self)
        if newxp >= xp_required:
            addlevel(self)
            self.xp = newxp - xp_required
        else:
            self.xp = newxp

    def setxp(self, exp):
        self.xp += exp





class FisBot(commands.Bot):
    bot = commands.Bot(command_prefix=commands.when_mentioned_or("."))
    users = []

    async def __init__(self, command_prefix, help_command=_default, description=None, **options):
        super().__init__(command_prefix, help_command=help_command, description=description, **options)

    pass




bot = commands.Bot(command_prefix=commands.when_mentioned_or("."))

bot.remove_command('help')


#songs = asyncio.Queue()
#play_next_song = asyncio.Event()
#bot.loop.create_task(bot_events.audio_player_task())

# Token read and run bot
with open("token.txt", "r") as token_file:
    bot.run(str(token_file.read()))