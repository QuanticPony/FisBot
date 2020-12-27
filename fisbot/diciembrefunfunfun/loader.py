from .funfunfun import HaceGracia

def setup(bot):
    bot.add_cog(HaceGracia(bot))

def teardown(bot):
    bot.remove_cog('EquisDe')