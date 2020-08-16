import discord
import asyncio
import random
from discord.ext import commands
from ..classes.bot_class import context_is_admin

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
        brief='''**ESTE COMANDO VA A CAMBIAR EN ALGUN MOMENTO 101%**''',
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
    )
    async def delete(self, context):
        if self.last_tipo == 'text':
            await self.dtc(context)

        if self.last_tipo == 'voice':
            await self.dvc(context)

    
    @category.command(
        hidden=True,
        pass_context=True, 
        aliases=['r'],
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
                await context.send("Bravo campeón")
                return
            else:
                await context.channel.purge(limit=int(float(amount[0]))+1, check=check)
        
    #@commands.command(
    #    hidden=True,
    #    pass_context=True, 
    #    help='''Crea canal de texto en la categoría donde se envió el mensaje con el nombre especificado''',
    #    brief='''Create Text Channel''',
    #    description='''COMANDO .ctc''',
    #)
    async def ctc(self, context, name):
        if not name:
            await context.message.channel.send('''Es necesario <name>''')
        else:
            category = context.message.channel.category
            await category.create_text_channel(name=name)
        return

    #@commands.command(
    #    hidden=True,
    #    pass_context=True, 
    #    help='''Borra el canal de texto donde se envió el mensaje''',
    #    brief='''Remove Text Channel''',
    #    description='''COMANDO .dtc''',
    #)
    async def dtc(self, context):
        if context_is_admin(context):
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

    #@commands.command(
    #    hidden=True,
    #    pass_context=True, 
    #    help='''Crea canal de voz con el nombre especificado en la categoría donde se encuentra el autor del mensaje''',
    #    brief='''Create Voice Channel''',
    #    description='''COMANDO .cvc''',
    #)
    async def cvc(self, context, name):
        if not name:
            await context.message.channel.send('''Es necesario <name>''')
        else:
            channel = context.message.author.voice.channel
            await channel.category.create_voice_channel(name=name)

    #@commands.command(
    #    hidden=True,
    #    pass_context=True, 
    #    help='''Elimina el canal de voz en el que se encuentra el usuario al enviar el mensaje''',
    #    brief='''Remove Voice Channel''',
    #    description='''COMANDO .dvc''',
    #)
    async def dvc(self, context: commands.Context):
        if context_is_admin(context):
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

    #@commands.command(pass_context=True)
    #async def subnormal(self, context, member, *thing):
    #    '''Manda un mensaje tts y le llama a <member> [thing] de tu parte, de nada'''
    #    user_origin = context.message.author
    #    user_destination = context.message.mentions[0]
    #    lil_frase = ''
    #    for thong in thing:
    #        lil_frase += ' '
    #        lil_frase += thong
    #    frase = "Hola {0.mention}.\n".format(user_destination) 
    #    frase += "Quería decirte de parte de {0.name}".format(user_origin) 
    #    frase += " que eres" 
    #    frase += lil_frase 
    #    frase += ".\nDe nada😎"
    #    await context.send(frase, tts=True)
    #    await context.message.delete()



    @commands.command(
        pass_context=True, 
        help='''¿No escucha a Jose y tiene que cambiarlo a otro canal y de vuelta?```.jose```
        ¿Quiere cambiar a otro canal y de vuelta a una persona en concreto?```.jose @member```
        ¿Quiere cambiar a otro canal y de vuelta a todo el mundo conectado?```.jose @everyone```''',
        brief='''Jovial Olor a Separacion Espontanea''',
        description='''Cambia a [member...] de canal de voz y lo vuelve a poner donde estaba. En el caso defaul cambia a Jose''',
        usage='.jose [member|role|group]'
    )
    async def jose(self, context, *member):
        if context_is_admin(context):
            jose = discord.Member
            if len(member) == 0:
                for memb in context.guild.members:
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

            channels = context.guild.channels
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
