import discord
import asyncio
from discord.ext import commands




                    





#TODO: 
#class music_boy(commands.Cog):
#    def __init__(self, bot):
#        self.bot = bot
#
#    @commands.command(pass_context=True)
#    async def play(self, context, url):
#        def toggle_next():
#            bot.loop.call_soon_threadsafe(play_next_song.set)
#
#        if not bot.is_voice_connected(context.message.server):
#            voice = await bot.join_voice_channel(context.message.author.voice_channel)
#        else:
#            voice = bot.voice_bot_in(context.message.server)
#
#        player = await voice.create_ytdl_player(url, after=toggle_next)
#        await songs.put(player)
#
#    @commands.command(pass_context=True)
#    async def join(self, context):
#        '''El bot entra en el canal de voz'''
#        await context.message.author.voice.channel.connect()
#
#    @commands.command(pass_context=True)
#    async def leave(self, context):
#        '''El bot sale del canal de voz'''
#        voice_client = bot.voice_client_in(context.message.server)
#        await voice_client.disconnect()
#
#



def setup(bot):
    print('commandos cargados')
    bot.add_cog(channels(bot))

def teardown(bot):
    print('commandos descargados')
    bot.remove_cog(channels)