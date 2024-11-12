from .task_cog import task_commands

async def setup(bot):
    await bot.add_cog(task_commands(bot))
    
async def teardown(bot):
    await bot.remove_cog('Trabajos y Examenes')