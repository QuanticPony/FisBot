from .tareas_cog import tareas_commands

def setup(bot):
    bot.add_cog(tareas_commands(bot))
    
def teardown(bot):
    bot.remove_cog('Trabajos')