from .funfunfun import HaceGracia

async def setup(bot):
    await bot.add_cog(HaceGracia(bot))

async def teardown(bot):
    await bot.remove_cog('EquisDe')