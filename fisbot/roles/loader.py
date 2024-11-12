from .custom_roles import custom_roles_cog

async def setup(bot):
    await bot.add_cog(custom_roles_cog(bot))
    
async def teardown(bot):
    await bot.remove_cog('Roles')