import discord
import asyncio
from discord.ext import commands


def context_is_admin(context):
    '''Devuelve True si el author del contexto que activa cierta funcion del Bot tiene permisos de administrador en dicho Servidor.
    Esta funcion se puede importar a otras extensiones para ponerla como check de commandos y cogs'''
    return context.message.author.guild_permissions.administrator




# Este es el envoltorio de la clase bot de discord: commands.bot
# Aqui puedes ver facilmente como se define un objeto. Es facil, pero al principio lia un poco:
# class <nobmre>(si hereda de algo):  
#     Heredar quiere decir que es el mismo objeto pero le puedes poner cosas extra: definir funciones y añadirle
#     mas variables.
#     Toda funcione definida dentro de una clase (objeto) debe llevar como primer parametro a si mismo: (self, ...)
# 
#     def __init__(self, ...):
#         Toda clase debe tener la funcion __init__. Esta inicializa el objeto. 
#         Cada uno de los elementos que empeizan por self. son variables que se le añaden al bot, como la lista de extensiones.

class FisBot(commands.Bot):    

    def __init__(self, command_prefix: str):
        # La siguiente funcion hace que nuestra nueva clase tenga todas las cosas de commands.bot. Esto hay que empollarlo
        super().__init__(command_prefix=commands.when_mentioned_or("."))

        # Asi se define una variable dentro de una clase y se inicializa a un valor
        self.extensions_list = [
            'help_command', # Esta extension tiene la implementacion del comando .help
            'default_cogs', # Esta extension tiene muchos comandos basicos

            'pruebas',      # ESTA EXTENSION ES LA RECOMENDADA PARA QUE HAGAS PRUEBAS Y APRENDAS A EXCRIBIR COMANDOS
            
            #'music',       # Esta extension tiene todos los comandos relacionados con la musica. No te recomiendo que la uses
            #'custom_roles' # Esta extension esta en desarrollo
            ]

        # Con esto llamo a la funcion definida abajo que añade todas las extensiones de la lista de extensiones
        self.add_extensions(self.extensions_list)


    # Esto es una funcion que crea un mensaje de tipo discord.Embed para dar la vienvenida al servidor a alguien nuevo
    # def create_embed_hello(self, member):
    #     embed = discord.Embed(
    #         title='''Bienvenido al servidor **{0.guild.name}**, {0.name}:'''.format(member, member), 
    #         description='''El equipo de moderadores de {0.guild.name} esperamos que disfrute del servidor y le sea realmente útil.'''.format(member), 
    #         color=0x00ecff)
    #     embed.add_field(
    #         name="Antes de empezar:", 
    #         value='''Dicho esto, esperamos también que cumpla algunas **normas básicas**: sea **respetuoso** y pongase su **nombre real** (no sabemos quien es *xX_DraG0nSlayerr3_Xx*)''', 
    #         inline=False)
    #     embed.add_field(
    #         name='''Dudas?''',
    #         value='''Para más información sobre el servidor, su funcionamiento y todo lo que puede hacer en él, le sugerimos que visite los canales de la **categoría GENERAL**
    #         Si aun así tiene dudas, suele haber siempre al menos un miembro conectado que seguro puede ayudarle''',
    #         inline=False)
    #     embed.add_field(
    #         name='''Disfrute!''',
    #         value='''[Más informacion]({0})'''.format('https://www.youtube.com/watch?v=dQw4w9WgXcQ'),
    #         inline=False
    #     )
    #     return embed


    # Esto es un evento definido en la api de discord. Hace lo siguiente: cada vez que el bot esta completamente definido llama a una funcion llamada on_ready
    # de manera normal esta no tiene nada. Pero se puede reescribir volviendola a definir. Ahora cambia lo que pone debajo de su nombre por playing .help
    async def on_ready(self):
        await self.change_presence(status=discord.Status.online, activity=discord.Game(name=".help"))

    # Esto implementa una funcion de arriba create_embed_hello cuando entra alguien nuevo al servidor
    # async def on_member_join(self, member):
    #     hello_message = create_embed_hello(self, context.author)
    #     if not context.author.dm_channel:
    #         await context.author.create_dm()
    #     await context.author.dm_channel.send(embed=hello_message)
    #     await context.author.guild.system_channel.send('Bienvenido al servidor {0.guild.name}, {0.mention}'.format(context.author, context.author))


        


    # Estas funciones las he añadido yo para añadirle extensiones al bot. No son dificiles de entender y vienen explicadas. Es IMPORTANTE saber que estos 
    # NO SON COMANDOS DEL BOT. Son funciones que he añadido al bot y pueden ser llamadas en codigo, y solo en codigo
    
    def add_extension(self, extension_name):
        '''Añade una extension al Bot. Tiene que haber un archivo con el nombre introducido y el archivo deberia contener una funcion del siguiente estilo:\n
        def setup(bot):\n
        \t bot.add_cog(commands.Cog: ClassName(bot))
        \t <code>
        '''
        self.load_extension(extension_name)

    def add_extensions(self, extensions_names):
        '''Añade una lista de extensiones al Bot. Tiene que haber un archivo por cada elemento de la lista con el nombre introducido y cada archivo deberia contener una funcion del siguiente estilo:\n
        def setup(bot):\n
        \t bot.add_cog(commands.Cog: ClassName1(bot))
        \t <code>
        '''
        for extension_name in extensions_names:
            self.load_extension(extension_name)

    def del_extension(self, extension_name):
        '''Quita una extension al Bot. Tiene que haber un archivo con el nombre introducido y el archivo puede contener una funcion del siguiente estilo:\n
        def teardown(bot):\n
        \t <code>
        '''
        self.unload_extension(extension_name)
        
    def del_extensions(self, extensions_names):
        '''Quita una lista de extensiones al Bot. Tiene que haber un archivo por cada elemento de la lista con el nombre introducido y cada archivo puede contener una funcion del siguiente estilo:\n
        def terdown(bot):\n
        \t <code>
        '''
        for extension_name in extensions_names:
            self.unload_extension(extension_name)