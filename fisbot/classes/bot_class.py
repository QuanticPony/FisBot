import discord
import asyncio
from discord.ext import commands
from discord.ext.commands.bot import Bot
import time

class FisBot_reminder(commands.Bot):    

    def __init__(self, *, command_prefix: str = None, path: str = None, intents=None, owner_id=None):
        super().__init__(command_prefix=command_prefix if command_prefix else 'yonodeberiaserllamadoparanada', owner_id=owner_id, intents=intents)
        self.owner_id = owner_id
        self.BOT_PATH = path

    
    async def on_ready(self):
        fiscords = [g for g in self.guilds if g.name =='FisCord']
        for fiscord in fiscords:
            fiscord : discord.Guild
            for c in fiscord.channels:
                c: discord.guild.TextChannel
                if c.name == 'iniciar-sesion':
                    for m in c.members:
                        m: discord.Member
                        if m.id == self.owner_id or m.id==370662132712341504:# or len(m.roles)==0 or:
                            dm_c = m.dm_channel
                            if dm_c is None:
                                dm_c = await m.create_dm()
                            try:
                                await dm_c.send("""**Hola muy buenas**!, 
te recordamos que para acceder a todas las funcionalidades de FisCord es necesario tener un nombre estandar como está definido en las reglas.
Por si acaso no lo has visto, te incluímos un enlace para que puedas ir rápidamente y disfrutar del servidor con los demás.

**Te estamos esperando!**

https://discord.gg/ggkNBZfqtP

> El equipo de moderación de FisCord
(Este mensaje será enviado automáticamente y diariamente hasta que sea validado)
                                """)
                            except Exception as e:
                                current_time = time.localtime()
                                current_time = time.strftime('%d-%m-%Y', current_time)

                                await c.send(f"{m.mention}, expulsado por bloquearme el {current_time}.")
                                await fiscord.kick(m, reason="Bloquear a FisBot está muy feo por tu parte... Si le desbloqueas podrás volver a acceder")
        
        self.close()

    

class FisBot(commands.Bot):    

    def __init__(self, *, command_prefix: str, path: str, intents=None, owner_id=None):
        super().__init__(command_prefix=command_prefix if command_prefix else '.', owner_id=owner_id, intents=intents)
        self.owner_id = owner_id
        self.extensions_list = [
            'fisbot.basics.loader',
            'fisbot.custom_help.loader',
            'fisbot.task_commands.loader',
            'fisbot.roles.loader',
            ]
        self.add_extensions(self.extensions_list)
        self.BOT_PATH = path
        

    def add_extension(self, extension_name):
        '''Añade una extension al Bot. Tiene que haber un archivo con el nombre introducido y el archivo deberia contener una funcion del siguiente estilo:\n
        def setup(bot):
            bot.add_cog(commands.Cog: ClassName(bot))
            <code>
        '''
        self.load_extension(extension_name)

    def add_extensions(self, extensions_names):
        '''Añade una lista de extensiones al Bot. Tiene que haber un archivo por cada elemento de la lista con el nombre introducido y cada archivo deberia contener una funcion del siguiente estilo:\n
        def setup(bot):
            bot.add_cog(commands.Cog: ClassName1(bot))
            <code>
        '''
        for extenion_name in extensions_names:
            self.load_extension(extenion_name)

    def del_extension(self, extension_name):
        '''Quita una extension al Bot. Tiene que haber un archivo con el nombre introducido y el archivo puede contener una funcion del siguiente estilo:\n
        def teardown(bot):
            bot.remove_cog(cog_name: string)
            <code>
        '''
        self.unload_extension(extension_name)
        
    def del_extensions(self, extensions_names):
        '''Quita una lista de extensiones al Bot. Tiene que haber un archivo por cada elemento de la lista con el nombre introducido y cada archivo puede contener una funcion del siguiente estilo:\n
        def terdown(bot):
            bot.remove_cog(cog_name1: string)
            <code>
        '''
        for extenion_name in extensions_names:
            self.unload_extension(extenion_name)