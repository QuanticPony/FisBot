import bot_class
from custom_help import help_command
   
def setup(bot: bot_class.FisBot):
    bot.add_cog(help_commands(bot))