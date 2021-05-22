import discord
import asyncio
import random
from discord.ext import commands
from .. import context_is_admin

ID_JOSE = 230323162414317568

class channels_managment(
    commands.Cog,
    name='Canales'
    ):
    '''Esta categoria de comandos te permite crear, eliminar y renombrar canales y categorias de canales del servidor
    **Le sugerimos** que pruebe ```.help text```'''
    
    def __init__(self, bot):
        self.bot = bot
        self.last_tipo = ''
    
    #TODO: cambiar esto para que sea mas entendible

    @commands.group(
        pass_context=True, 
        aliases=['text','voice'],
        help='''
        ¿Quieres crear un canal de texto en la categoria donde enviase el mensaje? ```.text create <name>```
        ¿Quieres borrar un canal de voz, donde estas en el momento? ```.voice delete```
        ¿Quieres cambiar el nombre de la categoria donde esta el canal de texto donde enviaste el mensaje? ```.category rename <name>```
        ''',
        brief='''Disponible previsiblemente en 1.1.1''',
        description='''Permite modificar, crear y eliminar los canales y categorias del servidor:

        .text <create|delete|rename> [nombre]
            create: Crea un canal de texto en la categoria donde se envio el mensaje con el nombre dado
            delete: Borra el canal de texto donde se envio el mensaje
            rename: Renombra el canal de texto donde se envio el mensaje al nombre dado

        .voice <create|delete|rename> [nombre]
            create: Crea un canal de voz en la categoria donde esta el autor del mensaje. Si no esta en ninguna en la misma categoria del mensaje
            delete: Borra el canal de voz donde esta el autor del mensaje
            rename: Renombra  el canal de voz donde esta el autor del mensaje al nombre dado''',
        usage='''.<text|voice|category> <orden> [argumentos...]'''
    )
    @commands.guild_only()
    async def category(self, context):
        if context.invoked_subcommand is None:
            await context.send('Y que mas (.<category/text/voice> <orden> [argumentos...])')
        else:
            self.last_tipo = context.invoked_with

            
    
    @category.command(
        hidden=True,
        pass_context=True, 
        aliases=['c'],
        usage='.<category/text/voice> create <name>'
    )
    async def create(self, context, *name):
        if not name:
            await context.send('Y que mas (.<category/text/voice> create <name>)')
        if self.last_tipo == 'text':
            await self.ctc(context, name[0])

        if self.last_tipo == 'voice':
            await self.cvc(context, name[0])


    @category.command(
        hidden=True,
        pass_context=True, 
        aliases=['d'],
        checks=[context_is_admin]
    )
    async def delete(self, context):
        if self.last_tipo == 'text':
            await self.dtc(context)

        if self.last_tipo == 'voice':
            await self.dvc(context)

    

    # TODO: hacer esto
    @category.command(
        hidden=True,
        pass_context=True, 
        aliases=['r'],
        checks=[context_is_admin]
    )
    async def rename(self, context, name):
        if self.last_tipo == 'text':
            await self.rtc(context, name)

        if self.last_tipo == 'voice':
            await self.rvc(context, name)
    






    @commands.command(
        pass_context=True, 
        aliases=['elimine','borra','elimina'],
        help='''¿El del mensaje anterior ha ofendido a algun colectivo sensible? ```.purge -1```
        ¿El mensaje anterior (solo 1) es altamente ofensivo contra los pitufos? ```.purge```
        ¿Quiere borrar 23 mensajes?```.purge 23```''',
        brief='''Elimina mensajes''',
        description='''Elimina [amount] mensajes. Por defecto elmina el enviado y el anterior''',
        usage='.purge [amount]',
        checks=[context_is_admin]
    )
    async def purge(self, context, *amount):
        def check(msg):
            return True

        if not amount:
            await context.channel.purge(limit=2, check=check)
        else:
            if float(amount[0]) <= 0:
                await context.send("Bravo campeon")
                return
            else:
                await context.channel.purge(limit=int(float(amount[0]))+1, check=check)
        
    
    async def ctc(self, context, name):
        if not name:
            await context.message.channel.send('''Es necesario <name>''')
        else:
            category = context.message.channel.category
            await category.create_text_channel(name=name)
        return

    
    async def dtc(self, context):
        if context_is_admin(context):
            def confirm(reaction, user):
                return str(reaction.emoji) == '✅' and context.message.author == user
            msg_conf = await context.message.channel.send('''¿Esta seguro de que quiere borrar {.channel.mention}?\tSi: ✅\t No: ❌'''.format(context.message))
            await msg_conf.add_reaction("✅")
            await msg_conf.add_reaction("❌")
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=confirm)
            except asyncio.TimeoutError:
                await msg_conf.delete()
            else:
                await context.message.channel.delete()
            return

    
    async def cvc(self, context, name):
        if not name:
            await context.message.channel.send('''Es necesario <name>''')
        else:
            channel = context.message.author.voice.channel
            await channel.category.create_voice_channel(name=name)

    
    async def dvc(self, context: commands.Context):
        if context_is_admin(context):
            msg_conf = await context.message.channel.send("¿Esta seguro de que quiere borrar {.channel.mention}? Si: ✅   No: ❌".format(context.message.author.voice))
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




    @commands.command(
        pass_context=True, 
        help='''¿No escucha a Jose y tiene que cambiarlo a otro canal y de vuelta?```.jose```
        ¿Quiere cambiar a otro canal y de vuelta a una persona en concreto?```.jose @member```
        ¿Quiere cambiar a otro canal y de vuelta a todo el mundo conectado?```.jose @everyone```''',
        brief='''Jovial Olor a Separacion Espontanea''',
        description='''Cambia a [member...] de canal de voz y lo vuelve a poner donde estaba. En el caso defaul cambia a Jose''',
        usage='.jose [member|role|group]'
    )
    @commands.guild_only()
    @commands.check(context_is_admin)
    async def jose(self, context, *member):

        jose = []
        if context.message.mention_everyone:
            jose = context.guild.members 

        else:
            if not member:
                try:
                    jose = [context.guild.get_member_named('RainbowWarrior#3399')]
                except:
                    return

            if context.message.mentions:
                jose = context.message.mentions

            if context.message.role_mentions:
                role_list = context.message.role_mentions
                for role in role_list:
                    jose.append(role.members)

        channels = context.guild.channels
        try:
            await context.message.delete()
        except:
            pass

        for member in jose:
            for channel_destination in channels:
                if type(member.voice) == discord.VoiceState:
                        channel_origin = member.voice.channel
                        if channel_destination != channel_origin and str(channel_destination.type) == 'voice':
                            try:
                                await member.move_to(channel_destination)
                                await member.move_to(channel_origin)
                            except:
                                await context.send('lol no xd')
                                return
                            break
                        
    @commands.command(
        pass_context=True, 
        help='''¿El comando jose no te da la suficiente satisfacción?```.autojose```''',
        brief='''Jovial Olor a Separacion Espontanea Automática''',
        description='''Cambia a [member...] de canal de voz y lo vuelve a poner donde estaba, después de un precioso paseo. En el caso defaul cambia a Jose''',
        usage='.jose [member|role|group]'
    )
    @commands.guild_only()
    @commands.check(context_is_admin)
    async def autojose(self, context, *member):

        jose = []
        if context.message.mention_everyone:
            jose = context.guild.members 

        else:
            if not member:
                try:
                    jose = [context.guild.get_member_named('RainbowWarrior#3399')]
                except:
                    return

            if context.message.mentions:
                jose = context.message.mentions

            if context.message.role_mentions:
                role_list = context.message.role_mentions
                for role in role_list:
                    jose.append(role.members)

        channels = context.guild.channels
        try:
            await context.message.delete()
        except:
            pass
        
        channel_origin = {}

        for member in jose:
            channel_origin.update({member: member.voice.channel})
                
        for channel_destination in channels:
            for member in jose:
                channel_origin = member.voice.channel
                if type(member.voice) == discord.VoiceState:
                        if channel_destination != channel_origin[member] and str(channel_destination.type) == 'voice':
                            try:
                                await member.move_to(channel_destination)
                            except:
                                pass
        for member in jose:
            await member.move_to(channel_origin[member])