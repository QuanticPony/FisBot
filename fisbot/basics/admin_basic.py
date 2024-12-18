import asyncio
from os import name
import pickle
import random

import discord
from discord.ext import commands

from .. import context_is_admin, context_is_whitelisted
from ..classes import user_class
from ..classes.achievements_class import Achievements
from ..database import base

from subprocess import call
import logging

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
       hidden=True
    )
    async def funfunfun(self, context):
       if not context.author.id == self.bot.owner_id:
           return
       await self.bot.add_extension('fisbot.diciembrefunfunfun.loader')
    

    @commands.command(
       pass_context=True,
       hidden=True
    )
    async def nofunfunfun(self, context):
       if not context.author.id == self.bot.owner_id:
           return
       await self.bot.del_extension('fisbot.diciembrefunfunfun.loader')


    @commands.command(
        pass_context=True,
        hidden=True
    )
    async def check_owner_id(self, context):
        await context.send(f"{context.author.id} = {self.bot.owner_id()} ?")

    
    #@commands.command(
    #    pass_context=True,
    #    hidden=True
    #)
    #async def erase_database(self, context):
    #    if not context.author.id == 195810097023287296:
    #        return
#
    #    from ..classes.user_class import FisUser
#
    #    for member in context.guild.members:
    #        if member.bot:
    #            continue
    #        channel = member.dm_channel
    #        if not channel:
    #            channel = await member.create_dm()
#
    #        user = await FisUser.init_with_member(member, context=context)
    #        embed = await user.embed_show()
    #        embed: discord.Embed
    #        embed.clear_fields()
    #        if user.level < 1:
    #            continue
    #        embed.add_field(
    #            name='Nivel:',
    #            value=random.randint(-user.level, user.level-1),
    #            inline=True
    #        )
    #        embed.add_field(
    #            name='Experiencia:',
    #            value=f"{random.randint(-999999,999999)}/{user.xp_to_lvl_up()}",
    #            inline=True
    #        )
    #        embed.add_field(
    #            name='Karma:',
    #            value=random.randint(-500,500),
    #            inline=True
    #        )
    #        await channel.send('''**Hola muy buenas:** hemos detectado un fallo en mi codigo por el cual se ha reiniciado su nivel en el servidor.
    #Ya lo hemos corregido pero por desgracia no hemos podido utilizar el backup de la base de datos. Hemos intentado dejarlo igual a como estaba:''', embed=embed)
    


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

        if ctx.message.channel_mentions and text:
            channel = ctx.message.channel_mentions[0]
            words_list = text.split(' ')
            new_text = ' '.join(list(word for word in words_list if channel.mention not in word))
            await channel.send(new_text)
            return

        new_text = ' '.join(text.split(' '))
        try:
            await ctx.message.delete()
            await ctx.send(new_text)
        except commands.MissingPermissions:
            await ctx.send('No voy a hablar por ti lol')
        

    @commands.command(
        pass_context=True, 
        help=r'''¿Añadir felicitaciones de nivel? ```.add_new_level_message "{mention} ha subido a nivel {level}."```''',
        brief='''Añadir mensaje de felicitación''',
        description='''Añade un nuevo mensaje de felicitación por subir de nivel.''',
        usage='.add_new_level_message'
        )
    @commands.check(context_is_admin)
    async def add_new_level_message(self, ctx, text):
        with open(f".{self.bot.BOT_PATH}/fisbot/database/celebrations.txt", 'a', encoding='utf8') as file:
            file.write('\n'+text)

    @commands.command(
        pass_context=True, 
        help=r'''¿Añadir felicitaciones de nivel? ```.add_new_level_message "{mention} ha subido a nivel {level}."```''',
        brief='''Añadir mensaje de felicitación''',
        description='''Añade un nuevo mensaje de felicitación por subir de nivel.''',
        usage='.add_new_level_message'
        )
    @commands.check(context_is_admin)
    async def del_level_message_contains(self, ctx, text):
        buff_lines = []
        with open(f".{self.bot.BOT_PATH}/fisbot/database/celebrations.txt", 'r+', encoding='utf8') as file:
            lines = file.readlines()
            buff_lines = lines.copy()
            for i, line in enumerate(buff_lines):
                if text in line:
                    buff_lines.pop(i)

        with open(f".{self.bot.BOT_PATH}/fisbot/database/celebrations.txt", 'w', encoding='utf8') as file:
            file.writelines(buff_lines)

    @commands.command(
        pass_context=True, 
        help='''¿Quieres que FisBot diga algo a alguien? ```.tellto @Jose Buenos dias caballero```''',
        brief='''Habla a alguien como Fisbot''',
        description='''Hace a FisBot decir algo por mensajes directos a algun usuario''',
        usage='.tellto <user_mention> <text>'
        )
    @commands.check(context_is_admin)
    async def tellto(self, ctx, *, text):

        if ctx.message.mentions and text:
            member = ctx.message.mentions[0]
            words_list = text.split(' ')
            new_text = ' '.join(list(word for word in words_list if member.mention not in word))
            channel = member.dm_channel
            if not channel:
                channel = await member.create_dm()

            await channel.send(new_text)
        else:
            await self.say(ctx, text=text)


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
            if cog_name != 'fisbot.basics.loader' and check(arg, cog_name):
                await self.bot.reload_extension(cog_name)


        await ctx.message.add_reaction("🔄")
        await self.bot.reload_extension('fisbot.basics.loader')

    
    @commands.command(
        pass_context=True,
        hidden=True
    )
    async def names(self, context, args):

        await context.send(f"{context.author.id}, {self.bot.owner_id}")

        if not context.author.id == self.bot.owner_id:
            return
        
        if args=='do':
            members = context.guild.members

            shuffled_members = members.copy()
            random.shuffle(shuffled_members)

            change_log = [[(i.id, i.nick if i.nick else i.name), (j.id, j.nick if j.nick else j.name)] for i, j in zip(members, shuffled_members)]

            with open('change_log', 'wb') as changes_file:
                pickle.dump(change_log, changes_file)

            for i, j in change_log:
                one = context.guild.get_member(i[0])
                two = context.guild.get_member(j[0])
                if one and two:
                    try:
                        await two.edit(nick=i[1])
                    except:
                        pass
        
        if args=='revert':
            with open('change_log', 'rb') as changes_file:
                changes_log = pickle.load(changes_file)

                for i, j in changes_log:
                    one = context.guild.get_member(i[0])
                    two = context.guild.get_member(j[0])
                    if one and two:
                        try:
                            await two.edit(nick=j[1])
                        except:
                            pass

    
    @commands.group(
        pass_context=True,
        hidden=True
    )
    async def achievements(self, context):
        pass

    @achievements.command(
        pass_context=True,
        hidden=True
    )
    async def add(self, context, semester, year):

        members = context.message.mentions
        if context.message.mention_everyone:
            members = context.guild.members

        for member in members:
            fisuser = await user_class.FisUser.init_with_member(member)
            Achievements.add_achievement(fisuser, semester, year)
        await context.message.add_reaction("✔️")

    @achievements.command(
        pass_context=True,
        hidden=True
    )
    async def insert(self, context):

        members = context.message.mentions
        id_list=[]
        for member in members:
            id_list.append(member.id)
        from ..database.achievements import AchievementsDB
        AchievementsDB.insert_all(id_list)

        await context.message.add_reaction("✔️")

    # TODO: cambiar clase Achievements a tipo d
    #? No recuerdo qué es esto, lo dejo aquí por si alguien en el futuro lo adivina. En ese caso, que me lo diga. Gracias.


    @achievements.command(
        pass_context=True,
        hidden=True
    )
    async def extras(self, context, text):

        members = context.message.mentions
        achs = []
        for member in members:
            achs.append(Achievements.get_achievement(member))

        for ach in achs:
            ach.extras = text
            ach.update()
        await context.message.add_reaction("✔️")



    @commands.command(
        pass_context=True, 
        help='''¿Quiere añadir a alguien a la whitelist? ```.whitelist add @mention```
        ¿Quieres eliminar a alguien de la whitelist? ```.whitelist remove @mention```''',
        brief='''Añade o elimina miembros de la whitelist''',
        description='''Añade o elimina miembros de la whitelist''',
        usage='.whitelist <mode> <mention/s>'
    )
    @commands.check(context_is_admin)
    async def whitelist(self, context, mode):

        if context.message.mentions:
            
            if mode == "add":
                with open("whitelist.txt", "a") as file:
                    for mention in context.message.mentions:
                        file.writelines(f"{mention.name}={mention.id}\n")
                
        
            if mode == "remove":
                new_list = []

                with open("whitelist.txt", "r") as file:
                    list = file.readlines()

                    for line in list:

                        for mention in context.message.mentions:

                            if line.split("=")[-1] == f"{mention.id}\n":
                                break
                        else:
                            new_list.append(line)

                with open("whitelist.txt", "w") as file:
                    file.writelines(new_list)

            await context.message.add_reaction("✔️")



    @commands.command(
        pass_context=True, 
        help='''¿Quieres encender el servidor? ```.wake```''',
        brief='''Enciende el servidor''',
        description='''Enciende el servidor''',
        usage='.wake'
    )
    @commands.check(context_is_whitelisted)
    async def wake(self, ctx: discord.AppCommandContext):
        await self.inform_owner(ctx)
        logging.info(f".wake command lauched by {ctx.message.author.name}")
        call("./wake_server.sh", shell=True)


    

    async def inform_owner(self, ctx: discord.AppCommandContext):
        logging.info(f".{ctx.invoked_with} command lauched by {ctx.message.author.name}")

        me = await ctx.bot.fetch_user(self.bot.owner_id)

        channel = me.dm_channel
        if not channel:
            channel = await me.create_dm()

        await channel.send(f".{ctx.invoked_with} invoked by {ctx.message.author.name}, id={ctx.message.author.id}")

