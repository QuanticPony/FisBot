import discord
from random import randint
from discord.ext import commands
from ..database.users import UsersDB
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
        await self.bot.change_presence(status=discord.Status.online, activity=discord.Game(name=".help"))


    @commands.Cog.listener()
    async def on_message(self, message):
        '''Cuando recibe un mensaje sube de nivel al autor si cumple ciertas condiciones'''

        if message.author.bot or not message.guild:
            return
        confirm, user = UsersDB.last_message_cooldown(message.author.id)

        if confirm:
            user._disc_obj = message.author
            await user.addxp(self.bot, message.guild)
        else:
            user = await FisUser.init_with_member(message.author)
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        '''Cuando se actualiza el estado de voz de un miembro. 
        Sube la experiencia del usuario en funcion del tiempo en canal de voz'''


        def check_channel(state):
            if before.channel == before.guild.afk_channel:
                return False
            if '!' in before.channel.category.name:
                return False
            return True

        
        if after.channel and not before.channel:
            UsersDB.new_voice_join(member.id)

        if not after.channel and before.channel:
            if not check_channel(before):
                return
            amount, user = UsersDB.last_voice_join(member.id)
            if not user:
                user = await FisUser.init_with_member(member)
                UsersDB.add_user(user)
            try:
                level = FisUser.init_with_member(member).level
                if level < 5:
                    await user.addxp(member.guild, amount=(amount % (5 * (level + 1))))
                else:
                    await user.addxp(member.guild, amount=(amount % (30)))

            except:
                pass


    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''Añade al usuario que acaba de entrar en el servidor a la base de datos de usuarios'''

        user = await FisUser.init_with_member(member)
        
        if not member.dm_channel:
            await member.create_dm()
            
        hello_message = self.create_embed_hello(member)
        await member.dm_channel.send(embed=hello_message)
        await member.guild.system_channel.send('Bienvenido al servidor {0.guild.name}, {0.mention}!'.format(member))

        initial_roles = FisRol.database.get_rol(0)
        for rol in initial_roles:
            await rol.give_to(user, guild=self.bot.get_guild(rol.guild_id))


    async def _karma(self, mult, reaction, user):
        '''Aplica lo correspondiente para aumentar o disminuir el karma'''

        fis_user = await FisUser.init_with_member(reaction.message.author)

        if not fis_user:
            fis_user = FisUser(reaction.message.author.id)
            fis_user.database.add_user(fis_user)
        
        if reaction.emoji == '⬆️':
            fis_user.karma += 1 * mult
        elif reaction.emoji == '⬇️':
            fis_user.karma -= 1 * mult
        
        fis_user.database.update_user(fis_user)


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