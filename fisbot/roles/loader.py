from .custom_roles import custom_roles

def setup(bot):
    bot.add_cog(custom_roles(bot))

def teardown(bot):
    bot.remove_cog('Roles')