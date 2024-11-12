from .help_cog import help_commands
   
async def setup(bot):
    await bot.add_cog(help_commands(bot))

async def teardown(bot):
    await bot.remove_cog('Ayuda')