from .task_cog import task_commands

def setup(bot):
    bot.add_cog(task_commands(bot))
    
def teardown(bot):
    bot.remove_cog('Trabajos y Examenes')