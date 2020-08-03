import bot_class
from basics.admin_basic import admin_basic_commands
from basics.cog import cog_managment
from basics.channels import channels_managment
from basics.polls import poll

def setup(bot: bot_class.FisBot):
    bot.add_cog(extensions_managment(bot))
    bot.add_cog(admin_basic_commands(bot))
    bot.add_cog(cog_managment(bot))
    bot.add_cog(channels_managment(bot))
    bot.add_cog(poll(bot))