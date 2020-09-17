from .extensions import extensions_managment
from .admin_basic import admin_basic_commands
from .cog import cog_managment
from .channels import channels_managment
from .polls import poll_cog
from .listeners import listeners
from .users_commands import users_cog

def setup(bot):
    bot.add_cog(extensions_managment(bot))
    bot.add_cog(admin_basic_commands(bot))
    bot.add_cog(cog_managment(bot))
    bot.add_cog(channels_managment(bot))
    bot.add_cog(poll_cog(bot))
    bot.add_cog(listeners(bot))
    bot.add_cog(users_cog(bot))

    

def teardown(bot):
    bot.remove_cog('Comandos basicos')
    bot.remove_cog('Control de comandos')
    bot.remove_cog('Canales')
    bot.remove_cog('Encuestas')
    bot.remove_cog('Eventos')
    bot.remove_cog('Usuarios')
    bot.remove_cog('Control de extensiones')