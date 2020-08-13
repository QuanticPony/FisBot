from music_commands.music_cog import Music

def setup(bot):
    bot.add_cog(Music(bot))

def teardown(bot):
    bot.remove_cog('Musica')