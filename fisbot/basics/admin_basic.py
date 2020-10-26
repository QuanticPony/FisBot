import discord
import asyncio
import random
from discord.ext import commands
from ..classes.bot_class import context_is_admin

class admin_basic_commands(
    commands.Cog,
    name='Comandos basicos',
    ):
    '''Conjunto de comandos que permite la manipulación basica del bot'''
    
    def __init__(self, bot):
        self.bot = bot
        self.cog_check(context_is_admin)


    @commands.command(
        pass_context=True, 
        aliases=['estado','juego'],
        help='''¿Quiere cambiar el estado del bot a patatas? ```.status patatas```
        ¿Quieres reiniciar el estado del bot al por defecto? ```.status```''',
        brief='''Cambia el estado del bot''',
        description='''Cambia el estado del bot. En el caso default pone como estado .help''',
        usage='.status [estado]'
    )
    @commands.check(context_is_admin)
    async def status(self, context, *, game=None):
        if not game:
            game = context.prefix + 'help'
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=game))


    @commands.command(
        pass_context=True, 
        help='''¿Quieres que FisBot diga algo? ```.say Hello World```
        ¿Quieres que FisBot diga algo cierto canal de texto?```.say #bots Horld Wello''',
        brief='''Di algo como FisBot''',
        description='''Hace a FisBot decir algo tanto por el mismo canal como por otro, segun se especifique''',
        usage='.say [channel_mention] <text>'
    )
    @commands.check(context_is_admin)
    async def say(self, ctx, *, text):

        if ctx.message.channel_mentions:
            channel = ctx.message.channel_mentions[0]
            words_list = text.split()
            new_text = ' '.join(list(word for word in words_list if channel.mention not in word))
            await channel.send(new_text)
            return

        new_text = ' '.join(text)
        await ctx.message.delete()
        await ctx.send(new_text)


    @commands.command(
        pass_context=True, 
        help='''¿Quieres que FisBot diga algo a alguien? ```.tellto @Jose Buenos dias caballero```''',
        brief='''Habla a alguien como Fisbot''',
        description='''Hace a FisBot decir algo por mensajes directos a algun usuario''',
        usage='.tellto <user_mention> <text>'
        )
    @commands.check(context_is_admin)
    async def tellto(self, ctx, *, text):

        if ctx.message.author:
            member = ctx.message.mentions[0]
            words_list = text.split()
            new_text = ' '.join(list(word for word in words_list if member.mention not in word))
            channel = member.dm_channel
            if not channel:
                channel = await member.create_dm()

            await channel.send(new_text)


    @commands.command(
        pass_context=True, 
        aliases=['noticia'],
        help='''¿Quiere publicar una noticia en el servidor? ```.news Esta es una noticia```''',
        brief='''Envia una noticia''',
        description='''Envía una noticia por el primer canal de noticias que encuentre''',
        usage='.news <message>'
    )
    @commands.check(context_is_admin)
    async def news(self, ctx, *, text):

        for channel in ctx.guild.text_channels:
            if channel.is_news():
                await channel.send(text)
                return


    @commands.command(
        pass_context=True, 
        aliases=['sd', 'shut', 'apagar'],
        help='''¿Quiere apagar el bot? No lo haga si no es imprescindible, pero se hace asi: ```.shutdown```''',
        brief='''Apaga el bot''',
        description='''Apaga el bot. No lo haga si no es imprescindible''',
        usage='.shutdown'
    )
    @commands.check(context_is_admin)
    async def shutdown(self, ctx):
        await self.bot.logout()
    
    
    @commands.command(
        pass_context=True, 
        aliases=['reset','restart', 'reiniciar'],
        help='''¿Se ha cambiado alguna libreria del bot y quiere actualizar su configuracion no imprescindible? ```.reload```
        ¿Quieres y necesitas reiniciar, pero tienes la musica activada y no te apetece volverle a pedir que reproduzca?```.restart -music```''',
        brief='''Recarga el bot''',
        description='''Recarga el bot y actualiza los comandos de todas las extensiones habilitadas''',
        usage='.reload',
    )
    @commands.check(context_is_admin)
    async def reload(self, ctx, *arg):
        if arg:
            arg[0] = arg[0].strip('-')

        def check(arg, cog_name):
            if not arg:
                return True
            else:
                return arg[0] in cog_name

        for cog_name in self.bot.extensions_list:
            if cog_name != 'fisbot.basics.loader' and check:
                self.bot.reload_extension(cog_name)


        await ctx.message.add_reaction("🔄")
        self.bot.reload_extension('fisbot.basics.loader')