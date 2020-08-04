from custom_help.help_cog import help_commands
   
def setup(bot):
    bot.add_cog(help_commands(bot))