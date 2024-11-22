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

class server_cog(
    commands.Cog,
    name='Servidor',
    ):
    '''Conjunto de comandos que permite la manipulación basica del servidor'''
    
    def __init__(self, bot):
        self.bot = bot
        self.cog_check(context_is_whitelisted)


    @commands.Cog.listener()
    async def on_ready(self):
        '''Cambia el estado a `Playing Factorio` cuando el bot esta listo'''

        await self.bot.change_presence(activity=discord.Game(name="Factorio"))

    @commands.command(
        pass_context=True, 
        aliases=['sd', 'shut', 'apagar'],
        help='''¿Quiere apagar el bot? No lo haga si no es imprescindible, pero se hace asi: ```.shutdown```''',
        brief='''Apaga el bot''',
        description='''Apaga el bot. No lo haga si no es imprescindible''',
        usage='.server shutdown'
    )
    async def shutdown(self, ctx):
        await self.inform_owner(ctx)
        logging.info(f".shutdown command lauched by {ctx.message.author.name}")
        call("./shutdown.sh", shell=True)
        await self.bot.logout()
    

    @commands.group(
        pass_context=True, 
        help='''Grupo de comandos para controlar el servidor de factorio''',
        brief='''Grupo de comandos de factorio''',
        description='''Grupo de comandos de factorio''',
        usage='.server factorio'
    )
    async def factorio(self, ctx: discord.AppCommandContext):
        pass

    @factorio.command(
        pass_context=True, 
        aliases=['start'],
        help='''¿Quieres encender el servidor de Factorio? ```.server factorio start```''',
        brief='''Arranca el servidor de Factorio''',
        description='''Arranca el servidor de Factorio''',
        usage='.server factorio start'
    )
    async def start(self, ctx: discord.AppCommandContext):
        await self.inform_owner(ctx)
        logging.info(f".server factorio start command lauched by {ctx.message.author.name}")
        call("./start_factorio_server.sh", shell=True)


    @factorio.command(
        pass_context=True, 
        aliases=['stop'],
        help='''¿Quieres apagar el servidor de Factorio? ```.server factorio stop```''',
        brief='''Para el servidor de Factorio''',
        description='''Para el servidor de Factorio''',
        usage='.server factorio stop'
    )
    async def stop(self, ctx: discord.AppCommandContext):
        await self.inform_owner(ctx)
        logging.info(f".server factorio stop command lauched by {ctx.message.author.name}")
        call("./stop_factorio_server.sh", shell=True)


    @factorio.command(
        pass_context=True, 
        aliases=['restart'],
        help='''¿Quieres reiniciar el servidor de Factorio? ```.server factorio stop```''',
        brief='''Reinicia el servidor de Factorio''',
        description='''Reinicia el servidor de Factorio''',
        usage='.server factorio restart'
    )
    async def restart(self, ctx: discord.AppCommandContext):
        await self.inform_owner(ctx)
        logging.info(f".server factorio restart command lauched by {ctx.message.author.name}")
        call("./restart_factorio_server.sh", shell=True)


    async def inform_owner(self, ctx: discord.AppCommandContext):
        logging.info(f".{ctx.invoked_with} command lauched by {ctx.message.author.name}")

        me = await ctx.bot.fetch_user(self.bot.owner_id)

        channel = me.dm_channel
        if not channel:
            channel = await me.create_dm()

        await channel.send(f".{ctx.invoked_with} invoked by {ctx.message.author.name}, id={ctx.message.author.id}")

