import discord
from discord.ext import commands
from ..database.users import UsersDB
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

        if message.author.bot:
            return
        bd = UsersDB()
        if bd.last_message_cooldown(message.author.id):
            user = bd.get_user(message.author.id)
            level = user.addxp()
            if level:
                await message.guild.system_channel.send(f"Buena {message.author.mention}!! Alguien ha subido al nivel {level}...")
            bd.update_user(user)
        return

    @commands.Cog.listener()
    async def on_member_join(self, member):
        '''Añade al usuario que acaba de entrar en el servidor a la base de datos de usuarios'''

        from ..database.users import UsersDB
        from ..classes.user_class import FisUser
        bd = UsersDB()

        if member.nick:
            user = FisUser(member.id, member.nick)
        else:
            user = FisUser(member.id, member.name)

        bd.add_user(user)

        
        if not member.dm_channel:
            await member.create_dm()
            
        hello_message = self.bot.create_embed_hello(self, member)
        await member.dm_channel.send(embed=hello_message)
        await member.guild.system_channel.send('Bienvenido al servidor {0.guild.name}, {0.mention}'.format(member))

    