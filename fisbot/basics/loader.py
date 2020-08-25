from .extensions import extensions_managment
from .admin_basic import admin_basic_commands
from .cog import cog_managment
from .channels import channels_managment
from .polls import poll
from .listeners import listeners

def setup(bot):
    bot.add_cog(extensions_managment(bot))
    bot.add_cog(admin_basic_commands(bot))
    bot.add_cog(cog_managment(bot))
    bot.add_cog(channels_managment(bot))
    bot.add_cog(poll(bot))
    bot.add_cog(listeners(bot))

    

def teardown(bot):
    bot.remove_cog('Control de extensiones')
    bot.remove_cog('Comandos basicos')
    bot.remove_cog('Control de comandos')
    bot.remove_cog('Canales')
    bot.remove_cog('Encuestas')
    bot.remove_cog('Eventos')