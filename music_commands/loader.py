import bot_class
from music_commands.music_cog import Music

def setup(bot: bot_class.FisBot):
    bot.add_cog(Music(bot))