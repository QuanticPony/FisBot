from .music_cog import Music

async def setup(bot):
    await bot.add_cog(Music(bot))

async def teardown(bot):
    await bot.remove_cog('Musica')