import discord
import asyncio
from discord.ext import commands
from bot_class import context_is_admin

ID_JOSE = 230323162414317568

class admin_basic_commands(
    commands.Cog,
    name='Comandos basicos',
    ):
    '''[Admin required] Conjunto de comandos que permite la manipulación básica del bot'''
    
    def __init__(self, bot):
        self.bot = bot
        self.cog_check(context_is_admin)

    @commands.command(
        pass_context=True, 
        aliases=['estado','juego'],
        help='''Cambia el estado del bot. En el caso default pone como estado .help''',
        brief='''[Admin required]''',
        description='''COMANDO .status''',
    )
    async def status(self, context, game=None):
        if game == None:
            game = context.prefix + 'help'
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=game))


    @commands.command(
        pass_context=True, 
        aliases=['sd', 'shut', 'apagar', 'stop'],
        help='''Apaga el bot,''',
        brief='''[Admin required]''',
        description='''COMANDO .shutdown''',
    )
    async def shutdown(self, ctx):
        await self.bot.logout()
    
    
    @commands.command(
        pass_context=True, 
        aliases=['reset','restart', 'reiniciar'],
        help='''Recarga el bot y actualiza los comandos de todas las extensiones habilitadas''',
        brief='''[Admin required]''',
        description='''COMANDO .reload''',
        )
    async def reload(self, ctx):
        if ctx.message.author.guild_permissions.administrator == False:
             return
        for cog_name in self.bot.extensions_list:
            if cog_name != 'default_cogs':
                self.bot.reload_extension(cog_name)
        await ctx.message.add_reaction("🔄")
        self.bot.reload_extension('default_cogs')


class extensions_managment(
    commands.Cog,
    name='''Control de extensiones'''
    ):
    '''[Admin required] Conjunto de comandos que permite la manipulación de las extensiones del bot'''

    def __init__(self, bot):
        self.bot = bot
        self.cog_check(context_is_admin)

    #@_cog_special_method
    #def cog_check(self, ctx):
    #    return ctx.message.author.guild_permissions.administrator

    @commands.command(
        pass_context=True, 
        aliases=['ext'],
        help='''Permite la manipulación de las extensiones del bot. Las diferentes ordenes son:
        \nenabled\t\t\t Muestra las extensiones habilitada
        \nload\t[extension]\t Carga la extensión [extension]
        \nreload\t[extension]\t Recarga la extensión [extension]
        \nunload\t[extension]\t Descarga la extensión [extension]
        ''',
        brief='''[Admin required]''',
        description='''COMANDO .extensions''',
    )
    async def extensions(self, ctx, order, *extension):
        if ctx.message.author.guild_permissions.administrator == False:
            await ctx.message.add_reaction("❌")
            return
        #print(orden)
        #print(str(extension[0]))

        if order == 'enabled':
            enabled_extensions = '```\n'

            for cog_name in self.bot.extensions_list:
                enabled_extensions += cog_name + '\n'
            else:
                enabled_extensions += '```'

            if enabled_extensions != '':
                await ctx.send(enabled_extensions)
        
        if order == 'load':
            self.bot.extensions_list.append(extension[0])
            self.bot.load_extension(extension[0])
            await ctx.message.add_reaction("✅")
        
        if order == 'reload':
            self.bot.reload_extension(extension[0])
            await ctx.message.add_reaction("🔄")
        
        if order == 'unload' and extension != 'extension_managment':
            self.bot.extensions_list.remove(extension[0])
            self.bot.unload_extension(extension[0])
            await ctx.message.add_reaction("❌")


#TODO: Arreglar esto. No funciona
class cog_managment(
    commands.Cog,
    name='''Control de comandos'''
    ):
    '''[Admin required] Conjunto de comandos que permite la manipulación de los conjuntos de commandos del bot'''

    def __init__(self, bot):
        self.bot = bot
        self.cog_check(context_is_admin)

    @commands.group(
        pass_context=True, 
        help='''
        Permite cargar, descargar las categorias de comandos de manera independiente de las extensiones a las que pertenezcan.
        Si no se invoca un subcomando escribe una lista con las categorias habilitadas.
        ''',
        brief='''[Admin required]''',
        description='''COMANDO .cog''',
    )
    async def cog(self, context):
        if context.invoked_subcommand is None:
            message = '```\n'
            for key in self.bot.cogs.keys():
                message += key + '\n' 
            else:
                message += '```'
            await context.send(message)
    


    #TODO: Preguntar a Aitor a ver como podría hacer esto. La otra froma es hacer un diccionario de todos los cogs posibles.
    @cog.command(
        pass_context=True, 
        help='''
        Permite cargar categorias de comandos
        ''',
        brief='''Permite cargar categorias de comandos''',
        description='''COMANDO .cog add''',
    )
    async def add(self, context, *cog_name):
        if cog_name is None:
            await context.send('Invalid Syntax: cog add <cog name>')
        else:
            for objeto in globals().values():
                if hasattr(objeto,'__bases__'):
                    if commands.Cog in objeto.__bases__:
                        if hasattr(objeto,'name'):
                            if objeto.name is cog_name:
                                self.bot.add_cog(objeto(self.bot))

    @cog.command(
        pass_context=True,
        help='''
        Permite cargar categorias de comandos
        ''',
        aliases=['del'],
        brief='''Permite descargar categorias de comandos''',
        description='''COMANDO .cog remove''',
    )
    async def remove(self, context, cog_name):
        if cog_name in self.bot.cogs:
            self.bot.remove_cog(cog_name)
        else:
            await context.send('No existe la categoria de comandos '+ cog_name + ', o no esta cargada')



                    



class channels_managment(
    commands.Cog,
    name='Canales'
    ):
    '''Conjunto de comandos que permiten manipular los canales y categorias. Incluye alguna funcionalidad de interaccion con usuarios'''
    
    def __init__(self, bot):
        self.bot = bot
        self.last_tipo = ''
    


    @commands.group(
        pass_context=True, 
        aliases=['text','voice'],
        help='''
        Permite modificar, crear y eliminar los canales y categorias del servidor:

        .text <create|delete|rename> [nombre]
            create: Crea un canal de texto en la categoria donde se envio el mensaje con el nombre dado
            delete: Borra el canal de texto donde se envio el mensaje
            rename: Renombra el canal de texto donde se envio el mensaje al nombre dado

        .voice <create|delete|rename> [nombre]
            create: Crea un canal de voz en la categoria donde esta el autor del mensaje. Si no esta en ninguna en la misma categoria del mensaje
            delete: Borra el canal de voz donde esta el autor del mensaje
            rename: Renombra  el canal de voz donde esta el autor del mensaje al nombre dado
        ''',
        brief='''.help text / .help voice''',
        description='''COMANDO .category / .text / .voice''',
        usage='<orden> [argumentos...]'
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
        usage='<name>'
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
        help='''Elimina [amount] mensajes. Por defecto elmina el enviado y el anterior''',
        brief='''[Admin required]''',
        description='''COMANDO .purge''',
        checks=[context_is_admin]
    )
    async def purge(self, context, *amount):
        if float(amount[0]) <= 0:
            await context.send("Bravo campeón")
            return
        def check(msg):
            return True
        if context.message.author.guild_permissions.administrator:
            if len(amount) == 0:
                await context.channel.purge(limit=2, check=check)
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
        help='''Cambia a [member...] de canal de voz y lo vuelve a poner donde estaba. En el caso defaul cambia a Jose''',
        brief='''Jovial Olor a Separacion Espontanea''',
        description='''COMANDO .jose''',
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


class users_managment(
    commands.Cog, 
    name='move commands',
    ):
    '''Conjunto de comandos que permite manipular a los usuarios en los canales de voz'''

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def move(self, context, order):
        pass



class poll(
    commands.Cog, 
    name='Encuestas',
    ):
    '''Comandos para realizar encuestas'''

    def __init__(self, bot):
        self.bot = bot
        self.sep = '_'
    
    @commands.command(
        pass_context=True, 
        aliases=['encuesta','p'],
        help='''Hace una encuesta entre todos los elementos separados por el separador''',
        brief='''Hace una encuesta''',
        description='''COMANDO .poll''',
    )
    async def poll(self, context, *, elementos):
        things_list = elementos.split(self.sep)
        print(things_list)
        

    @commands.command(
        pass_context=True, 
        aliases=['pollsep','sep','separador'],
        help='''Cambia la string de separacion de elementos de encuesta en el comando .poll''',
        brief='''Cambia el separador de .poll''',
        description='''COMANDO .separator''',
    )
    async def separator(self, context, *separator):
        if separator:
            self.sep = separator[0]
        else:
            await context.send('Actualmente el prefijo de .poll es \'{0.sep}\''.format(self))



    

def setup(bot):
    bot.add_cog(extensions_managment(bot))
    bot.add_cog(admin_basic_commands(bot))
    bot.add_cog(cog_managment(bot))
    bot.add_cog(channels_managment(bot))
    #bot.add_cog(users_managment(bot))
    bot.add_cog(poll(bot))
