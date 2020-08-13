import discord
import asyncio
from discord.ext import commands
from custom_help.custom_help_implementation import custom_help_implementation_command
from custom_help.custom_help_implementation import custom_help_implementation_general

class help_commands(
    commands.Cog,
    name='Ayuda'
    ):
    '''¿Necesita informacion general del servidor y su estructura? ```.ayuda```
    ¿Necesitas ayuda porque no entiendes lo que hace o como se utiliza cierto comando o categoria de comandos? ```.help [command|category]```
    **Le recomendamos** que pruebe *.help help*'''

    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command('help')
        

    @commands.command(
        name='ayuda',
        brief='''Muestra informacion general del servidor''',
        description='''Te da informacion basica sobre el funcionamiento del servidor. Para informaicon de comandos y categorias prueba ```.help [command|category]```''',
        usage='.ayuda'
    )
    @commands.has_permissions(embed_links=True)
    async def _ayuda(self, ctx):
        ayuda=discord.Embed(
            title='Hola {.nick}:'.format(ctx.author),
            description='Vemos que has pedido ayuda en {0.channel.mention} sobre el servidor {0.guild.name}:'.format(ctx),
            color=discord.Color.gold()
        )
        ayuda.add_field(
            name='Normas basicas:',
            value='''1. Ser respetuoso
            2. Tener como nickname del servidor vuestro nombre real (al menos un apellido)''',
            inline=False
        )
        ayuda.add_field(
            name='Estructura del servidor:',
            value='''Este servidor esta estructurado en **categorias** de *dudas*, *trabajando*, *no trabajando*, *general* y algun *grupo de trabajo*.
            El nombre de las categorias ya explica de que va el tema de cada canal de texto o voz dentro de la misma. La categoria mas interesante es *general*:''',
            inline=False
        )
        
        for category in ctx.guild.categories:
             if category.name=='General':
                break

        for channel in category.text_channels:
            ayuda.add_field(
                name='**General**.*{.name}*:'.format(channel),
                value='''{0.mention}:
                {0.topic}'''.format(channel),
                inline=False
            )

        if not ctx.author.dm_channel:
            await ctx.author.create_dm()
        return await ctx.author.dm_channel.send(embed=ayuda)



    @commands.command(
        name='help',
        aliases=['h'],
        help='''¿Dudas sobre como poner musica? .help Musica
        ¿Duda sobre el comando .play? .help play''',
        brief='''Muestra informacion de categorias y comandos''',
        description='''Muestra la informacion disponible sobre el bot. Si no se introduce nada muestra todas las categorias y sus comandos con una breve descripcion. 
        Si se escribe seguido de una categoria muestra la informacion y comandos de ella. 
        Si se escribe seguido de un comando se muestra la informacion relativa al comando, funcionamiento y uso del mismo.
        Y si, tenemos tanto tiempo que hemos completado el comando .help help''',
        usage='.help [category|command]'
    )
    @commands.has_permissions(embed_links=True)
    async def _help(self, ctx, *nombre):
        if not nombre:
            await custom_help_implementation_general(self.bot, ctx)
        else:
            await custom_help_implementation(self.bot, ctx, ' '.join(nombre))