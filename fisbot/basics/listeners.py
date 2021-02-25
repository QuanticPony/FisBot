import discord
from time import time
from random import randint
from discord.ext import commands
from ..database.users import UsersDB
from ..database.roles import RolesDB
from ..classes.rol_class import FisRol
from ..classes.user_class import FisUser 

class listeners(
    commands.Cog,
    name='Eventos'
    ):
    def __init__(self, bot):
        self.bot = bot


    def create_embed_hello(self, member):
        embed = discord.Embed(
            title='''Bienvenido al servidor **{0.guild.name}**, {0.name}:'''.format(member), 
            description='''El equipo de moderadores de {.guild.name} esperamos que disfrute del servidor y le sea realmente util.'''.format(member), 
            color=0x00ecff)
        embed.add_field(
            name="Antes de empezar:", 
            value='''Dicho esto, esperamos tambien que cumpla algunas **normas basicas**: sea **respetuoso** y pongase su **nombre real** (no sabemos quien es *xX_DraG0nSlayerr3_Xx*)''', 
            inline=False)
        embed.add_field(
            name='''Dudas?''',
            value='''Para mas informacion sobre el servidor, su funcionamiento y todo lo que puede hacer en el, le sugerimos que visite los canales de la **categoria GENERAL**
            Si aun asi tiene dudas, suele haber siempre al menos un miembro conectado que seguro puede ayudarle''',
            inline=False)
        embed.add_field(
            name='''Disfrute!''',
            value='''[Mas informacion]({})'''.format('https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
            inline=False
        )
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        '''Cambia el estado a `Playing .help` cuando el bot esta listo'''
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f"{self.bot.command_prefix}help"))


    @commands.Cog.listener()
    async def on_message(self, message):
        '''Cuando recibe un mensaje sube de nivel al autor si cumple ciertas condiciones'''

        try:
            if message.author.bot or not message.guild:
                return
            time, user = FisUser.last_message_cooldown(message.author.id)
        except AttributeError:
            return
        
        try:
            if message.channel.category:
                if '!' in message.channel.category.name:
                    return 
        except:
            pass

        if user:
            user._disc_obj = message.author
            user:FisUser
            await user.addxp(self.bot, message.guild, time=time, amount_type='Text')

        else:
            UsersDB.add_user(FisUser(message.author.id, message.author.display_name, last_message=time()))
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        '''Cuando se actualiza el estado de voz de un miembro. 
        Sube la experiencia del usuario en funcion del tiempo en canal de voz'''

        if member.bot:
            return

        def check_channel(state):
            try:
                if before.channel == before.channel.guild.afk_channel:
                    return False
            except AttributeError:
                pass
            try:
                if '!' in before.channel.category.name:
                    return False
            except AttributeError:
                pass
            return True

        if after.channel and not before.channel:
            UsersDB.new_voice_join(member.id)

        if not after.channel and before.channel:
            if not check_channel(before):
                return

            g = before.channel.guild
            
            time, user_data = UsersDB.last_voice_join(member.id)
            user = FisUser(*user_data)
            UsersDB.new_voice_join(member.id)

            if not user:
                user = await FisUser.init_with_member(member)
                UsersDB.add_user(user)
            try:
                await user.addxp(self.bot, member.guild, time=time, amount_type='Voice') 
            except:
                pass


    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''Añade al usuario que acaba de entrar en el servidor a la base de datos de usuarios'''

        user = await FisUser.init_with_member(member)
        
        if not member.dm_channel:
            await member.create_dm()
            
        hello_message = self.create_embed_hello(member)

        await member.guild.system_channel.send('Bienvenido al servidor {0.guild.name}, {0.mention}!'.format(member))
        try:
            await member.dm_channel.send(embed=hello_message)
        except:
            await member.guild.system_channel.send(embed=hello_message)
        
        initial_roles = FisRol.convert_from_database(RolesDB.get_roles, (0, member.guild.id))
        if not isinstance(initial_roles, list):
            initial_roles = [initial_roles]
        for rol in initial_roles:
            await rol.give_to(user, guild=self.bot.get_guild(rol.guild_id))


    async def _karma(self, mult, reaction, user):
        '''Aplica lo correspondiente para aumentar o disminuir el karma'''

        fis_user = await FisUser.init_with_member(reaction.message.author)

        if not fis_user:
            fis_user = FisUser(reaction.message.author.id)
            UsersDB.add_user(fis_user)
        
        if reaction.emoji == '⬆️':
            fis_user.karma += 1 * mult
        elif reaction.emoji == '⬇️':
            fis_user.karma -= 1 * mult
        
        UsersDB.update_user(fis_user)


    def check_if_different(self, reaction, user):
        '''Comprueba que son usuarios diferentes. Para no poder ponerte karma a ti mismo'''

        return reaction.message.author.id != user.id


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        '''Si es un ⬆️ aumenta el karma del usuario. Si es un ⬇️ lo baja'''

        if self.check_if_different(reaction, user):
            await self._karma(1, reaction, user)


    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        '''Si es un ⬆️ disminuye el karma del usuario. Si es un ⬇️ lo aumenta'''

        if self.check_if_different(reaction, user):
            await self._karma(-1, reaction, user)