from .extensions import extensions_managment
from .admin_basic import admin_basic_commands
from .cog import cog_managment
from .channels import channels_managment
from .polls import poll

def setup(bot):
    bot.add_cog(extensions_managment(bot))
    bot.add_cog(admin_basic_commands(bot))
    bot.add_cog(cog_managment(bot))
    bot.add_cog(channels_managment(bot))
    bot.add_cog(poll(bot))

def teardown(bot):
    bot.remove_cog('Control de extensiones')
    bot.remove_cog('Comandos basicos')
    bot.remove_cog('Control de comandos')
    bot.remove_cog('Canales')
    bot.remove_cog('Encuestas')