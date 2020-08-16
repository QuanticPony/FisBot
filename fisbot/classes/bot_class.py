import discord
import asyncio
from discord.ext import commands


def context_is_admin(context):
    '''Devuelve True si el author del contexto que activa cierta funcion del Bot tiene permisos de administrador en dicho Servidor.
    Esta funcion se puede importar a otras extensiones para ponerla como check de commandos y cogs'''
    return context.message.author.guild_permissions.administrator


class FisBot(commands.Bot):    

    def __init__(self, command_prefix: str):
        super().__init__(command_prefix=commands.when_mentioned_or("."))
        self.extensions_list = [
            'fisbot.custom_help.loader',
            'fisbot.basics.loader',
            'fisbot.music_commands.loader',
            #'custom_roles'
            ]
        self.add_extensions(self.extensions_list)


    def create_embed_hello(self, member):
        embed = discord.Embed(
            title='''Bienvenido al servidor **{0.guild.name}**, {0.name}:'''.format(member, member), 
            description='''El equipo de moderadores de {0.guild.name} esperamos que disfrute del servidor y le sea realmente útil.'''.format(member), 
            color=0x00ecff)
        embed.add_field(
            name="Antes de empezar:", 
            value='''Dicho esto, esperamos también que cumpla algunas **normas básicas**: sea **respetuoso** y pongase su **nombre real** (no sabemos quien es *xX_DraG0nSlayerr3_Xx*)''', 
            inline=False)
        embed.add_field(
            name='''Dudas?''',
            value='''Para más información sobre el servidor, su funcionamiento y todo lo que puede hacer en él, le sugerimos que visite los canales de la **categoría GENERAL**
            Si aun así tiene dudas, suele haber siempre al menos un miembro conectado que seguro puede ayudarle''',
            inline=False)
        embed.add_field(
            name='''Disfrute!''',
            value='''[Más informacion]({0})'''.format('https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
            inline=False
        )
        return embed


    async def on_ready(self):
        await self.change_presence(status=discord.Status.online, activity=discord.Game(name=".help"))



    async def on_member_join(self, member):
        from ..database.users import UsersDB
        from ..classes.user_class import FisUser
        bd = UsersDB()
        if member.nick:
            user = FisUser(member.id, member.nick)
        else:
            user = FisUser(member.id, member.name)
        bd.add_user(user)

        hello_message = create_embed_hello(self, context.author)
        if not context.author.dm_channel:
            await context.author.create_dm()
        await context.author.dm_channel.send(embed=hello_message)
        await context.author.guild.system_channel.send('Bienvenido al servidor {0.guild.name}, {0.mention}'.format(context.author, context.author))


        
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