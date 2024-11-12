from .extensions import extensions_managment
from .admin_basic import admin_basic_commands
from .cog import cog_managment
from .channels import channels_managment
from .polls import poll_cog
from .listeners import listeners
from .users_commands import users_cog

async def setup(bot):
    await bot.add_cog(extensions_managment(bot))
    await bot.add_cog(admin_basic_commands(bot))
    # await bot.add_cog(cog_managment(bot))
    await bot.add_cog(channels_managment(bot))
    await bot.add_cog(poll_cog(bot))
    await bot.add_cog(listeners(bot))
    await bot.add_cog(users_cog(bot))

    

async def teardown(bot):
    await bot.remove_cog('Comandos:_basicos')
    # await bot.remove_cog('Control de comandos')
    await bot.remove_cog('Canales')
    await bot.remove_cog('Encuestas')
    await bot.remove_cog('Eventos')
    await bot.remove_cog('Usuarios')
    await bot.remove_cog('Control de extensiones')