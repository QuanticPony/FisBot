import discord
import asyncio
from discord.ext import commands
from bot_class import context_is_admin

ID_JOSE = 230323162414317568

class admin_basic_commands(
    commands.Cog,
    name='[Admin] Comandos basicos',
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
        aliases=['restart', 'reiniciar'],
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
    name='''[Admin] Control de extensiones'''
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


class cog_managment(
    commands.Cog,
    name='''Control de extensiones'''
    ):
    '''[Admin required] Conjunto de comandos que permite la manipulación de los conjuntos de commandos del bot'''

    def __init__(self, bot):
        self.bot = bot
        self.cog_check(context_is_admin)

    @commands.group(
        pass_context=True, 
        help='''Sub commandos disponibles:
        \nadd\t\t\t Muestra las extensiones habilitada
        \nd\t[extension]\t Carga la extensión [extension]
        \nreload\t[extension]\t Recarga la extensión [extension]
        \nunload\t[extension]\t Descarga la extensión [extension]
        ''',
        brief='''[Admin required]''',
        description='''COMANDO .status''',
    )
    async def cog(self, context):
        if context.invoked_subcommands is None:
            await context.send('Invalid Syntax: cog <sub_command> [args...]')
    


    #TODO: Preguntar a Aitor a ver como podría hacer esto. La otra froma es hacer un diccionario de todos los cogs posibles.
    @cog.command()
    async def add(self, context, cog_name):
        if cog_name is None:
             await context.send('Invalid Syntax: cog add <cog name>')
        else:
            if globals().have_key(cog_name):
                self.bot.add_cog(globals()[cog_name].__init__(self.bot))
                    



class channels_managment(
    commands.Cog,
    name='Canales'
    ):
    '''Conjunto de comandos que permiten manipular los canales, tanto crearlos como eliminarlos'''
    
    def __init__(self, bot):
        self.bot = bot
    
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
        
    @commands.command(
        pass_context=True, 
        help='''Crea canal de texto en la categoría donde se envió el mensaje con el nombre especificado''',
        brief='''Create Text Channel''',
        description='''COMANDO .ctc''',
    )
    async def ctc(self, context):
        try:
            prefix, name = context.message.content.split() 
        except ValueError:
            await context.message.channel.send("Especifica: .ctc \"name\" ")
        else:
            category = context.message.channel.category
            await category.create_text_channel(name=name)
        return

    @commands.command(
        pass_context=True, 
        help='''Borra el canal de texto donde se envió el mensaje''',
        brief='''Remove Text Channel''',
        description='''COMANDO .rtc''',
    )
    async def rtc(self, context):
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

    @commands.command(
        pass_context=True, 
        help='''Crea canal de voz con el nombre especificado en la categoría donde se encuentra el autor del mensaje''',
        brief='''Create Voice Channel''',
        description='''COMANDO .cvc''',
    )
    async def cvc(self, context):
        
        try:
            prefix, name = context.message.content.split()
        except ValueError:
            await context.message.channel.send('''Especifica: .cvc \"name\" ''')
        else:
            channel = context.message.author.voice.channel
            await channel.category.create_voice_channel(name=name)

    @commands.command(
        pass_context=True, 
        help='''Elimina el canal de voz en el que se encuentra el usuario al enviar el mensaje''',
        brief='''Remove Voice Channel''',
        description='''COMANDO .rvc''',
    )
    async def rvc(self, context: commands.Context):
        
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


    

def setup(bot):
    bot.add_cog(extensions_managment(bot))
    bot.add_cog(admin_basic_commands(bot))
    bot.add_cog(cog_managment(bot))
    bot.add_cog(channels_managment(bot))
    #bot.add_cog(users_managment(bot))
