from .server import server_cog

async def setup(bot):
    await bot.add_cog(server_cog(bot))

    

async def teardown(bot):
    await bot.remove_cog('Servidor')