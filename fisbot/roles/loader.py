from .custom_roles import custom_roles_cog

def setup(bot):
    bot.add_cog(custom_roles_cog(bot))

def teardown(bot):
    bot.remove_cog('Roles')