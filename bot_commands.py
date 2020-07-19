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
    async def subnormal(self, context, member, *thing):
        '''Manda un mensaje tts y le llama a <member> [thing] de tu parte, de nada'''
        user_origin = context.message.author
        user_destination = context.message.mentions[0]
        lil_frase = ''
        for thong in thing:
            lil_frase += ' '
            lil_frase += thong
        frase = "Hola {0.name}.\n".format(user_destination) 
        frase += "Quería decirte de parte de {0.name}".format(user_origin) 
        frase += " que eres" 
        frase += lil_frase 
        frase += ".\nDe nada😎"
        await context.send(frase, tts=True)
        await context.message.delete()



    @commands.command(pass_context=True)
    async def jose(self, context, *member):
        '''Cambia a [member] de canal de voz y lo vuelve a poner donde estaba. En el caso defaul cambia a Jose'''
        #if context.message.author.Permissions.administrator:
        channel1 = context.message.author.voice.channel
        jose = discord.Member
        if len(member) == 0:
            for memb in channel1.members:
                if memb.id == ID_JOSE:
                    jose = memb
                    break
        else:
            jose = context.message.mentions
            if len(jose) == 0:
                role_list = context.message.role_mentions
                jose.clear()
                for role in role_list:
                    jose.append(role.members)
            
            if len(jose) == 0:
                if context.message.mention_everyone:
                    jose = context.guild.members

        channels = context.message.author.voice.channel.category.channels
        await context.message.delete()

        if type(jose[0]) == list :
            for member in jose[0]:
                for channel_destination in channels:
                    if type(member.voice) == discord.VoiceState:
                        channel_origin = member.voice.channel
                        if channel_destination != channel_origin and str(channel_destination.type) == 'voice':
                            await member.move_to(channel_destination)
                            await member.move_to(channel_origin)
                            break
        else: 
            for channel_destination in channels:
                if type(jose[0].voice) == discord.VoiceState:
                    channel_origin = jose[0].voice.channel
                    if channel_destination != channel_origin and str(channel_destination.type) == 'voice':
                        await jose[0].move_to(channel_destination)
                        await jose[0].move_to(channel_origin)
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
    print('commandos cargados')
    bot.add_cog(channels(bot))

def teardown(bot):
    print('commandos descargados')
    bot.remove_cog(channels)