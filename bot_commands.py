import discord
import asyncio
from discord.ext import commands


class channels(commands.Cog):
    '''Conjunto de commandos que permiten manipular los canales, tanto crearlos como eliminarlos
    También permite cambiar rapidamente de canal de voz a Jose'''

    ID_JOSE = 230323162414317568
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(pass_context=True)
    async def ctc(self, context):
        '''Crea canal de texto en la categoría donde se envió el mensaje con el nombre especificado'''
        try:
            prefix, name = context.message.content.split() 
        except ValueError:
            await context.message.channel.send("Especifica: .ctc \"name\" ")
        else:
            category = context.message.channel.category
            await category.create_text_channel(name=name)
        return
    
    @commands.command(pass_context=True)
    async def ctc(self, context):
        '''Crea canal de texto con el nombre especificado en la categoría donde se envió el mensaje'''
        try:
            prefix, name = context.message.content.split() 
        except ValueError:
            await context.message.channel.send("Especifica: .ctc \"name\" ")
        else:
            category = context.message.channel.category
            await category.create_text_channel(name=name)
        return

    @commands.command(pass_context=True)
    async def rtc(self, context):
        '''Borra el canal de texto donde se envió el mensaje'''
        if context.message.author.guild_permissions.administrator:
            def confirm(reaction, user):
                return str(reaction.emoji) == '✅' and context.message.author == user
            msg_conf = await context.message.channel.send('''¿Está seguro de que quiere borrar {.channel.mention}?\tSi: ✅\t No: ❌'''.format(context.message))
            await msg_conf.add_reaction("✅")
            await msg_conf.add_reaction("❌")
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=confirm)
            except asyncio.TimeoutError:
                await msg_conf.delete()
            else:
                await context.message.channel.delete()
            return

    @commands.command(pass_context=True)
    async def cvc(self, context):
        '''Crea canal de voz con el nombre especificado en la categoría donde se encuentra el autor del mensaje'''
        try:
            prefix, name = context.message.content.split()
        except ValueError:
            await context.message.channel.send('''Especifica: .cvc \"name\" ''')
        else:
            channel = context.message.author.voice.channel
            await channel.category.create_voice_channel(name=name)

    @commands.command(pass_context=True)
    async def rvc(self, context: commands.Context):
        '''Elimina el canal de voz en el que se encuentra el usuario al enviar el mensaje'''
        if context.message.author.Permissions.administrator:
            msg_conf = await context.message.channel.send("¿Está seguro de que quiere borrar {.channel.mention}? Si: ✅   No: ❌".format(context.message.author.voice))
            await msg_conf.add_reaction("✅")
            await msg_conf.add_reaction("❌")

            def confirm(reaction, user):
                return str(reaction.emoji) == '✅' and context.message.author == user
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=confirm)
            except asyncio.TimeoutError:
                await msg_conf.delete()
            else:
                channel = context.message.author.voice.channel
                await msg_conf.delete()
                await channel.delete()


    @commands.command(pass_context=True)
    async def jose(self, context):
        '''Cambia a Jose de canal de voz y lo vuelve a poner donde estaba'''
        if context.message.author.Permissions.administrator:
            channel1 = context.message.author.voice.channel
            jose = discord.Member
            for memb in channel1.members:
                if memb.id == ID_JOSE:
                    jose = memb
                    break

            channels = context.message.author.voice.channel.category.channels
            for channel2 in channels:
                if channel2 != jose.voice.channel and str(channel2.type) == 'voice':
                    await jose.move_to(channel2)
                    await jose.move_to(channel1)
                    await context.message.delete()
                    break





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
    bot.add_cog(channels)









