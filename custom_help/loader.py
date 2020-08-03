import bot_class
from custom_help.help_cog import help_commands
   
def setup(bot: bot_class.FisBot):
    bot.add_cog(help_commands(bot))