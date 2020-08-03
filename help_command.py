import discord
import asyncio
from discord.ext import commands

# Este archivo tiene cosas de bastante complejidad. Recomiendo que no la modifiques y si tienes cualquier duda me preguntes

# Esta clase tiene la implementacion de todos los comandos de ayuda: .ayuda y .help.
# Te sirven para ver los comandos disponibles y una breve ayuda de los canales del servidor
# NO HAY ACLARACIONES DE COMO FUNCIONA ESTO. SI ESTAIS APRENDIENDO NO LO MIREIS
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
        description='''Te da informacion basica sobre el funcionamiento del servidor. Para informacion de comandos y categorias prueba ```.help [command|category]```''',
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
    # No se da ni categoria ni comando 
        if not nombre:  
            halp=discord.Embed(
                title='.help', 
                description='Estos son los comandos disponibles para {0.author.mention}:'.format(ctx), 
                color=discord.Color.green()
            )
            for cog in self.bot.cogs.values():
                commands_desc = ''
                for x in cog.get_commands():
                    if await x.can_run(ctx):
                        commands_desc += ('{0: <15} {1}'.format(x.name,x.brief) + '\n')

                if commands_desc:
                    halp.add_field(
                        name=cog.qualified_name,
                        value=commands_desc,
                        inline=False
                    )
            return await ctx.send(embed=halp)


    # Se da categoria o comando
        else:
            cog = self.bot.get_cog(' '.join(nombre))

        # Se da categoria
            if cog:
                commands_desc = ''
                for x in cog.get_commands():
                    if await x.can_run(ctx):
                        commands_desc += ('{0: <15} {1}'.format(x.name,x.brief) + '\n')

                if not commands_desc:
                    halp=discord.Embed(
                        title='Lo siento {0.author.mention}'.format(ctx),
                        description='No tienes permisos para utilizar ninguno de los comandos de la categoria {0}'.format(cog.qualified_name),
                        color=discord.Color.red()
                    )
                    return await ctx.send(embed=halp)

                else:
                    halp=discord.Embed(
                        title='.help {}'.format(cog.qualified_name), 
                        description=cog.__doc__,
                        color=discord.Color.blue()
                    )
                    halp.add_field(
                        name='Comandos de la categoria {0.qualified_name}:'.format(cog),
                        value=commands_desc,
                        inline=False
                    )
                    return await ctx.send(embed=halp)


            command = self.bot.get_command(' '.join(nombre))
        # Se da comando
            if command:
                halp=discord.Embed(
                        title='**{0.cog.qualified_name}**: *.{0.name}*'.format(command), 
                        description=command.brief,
                        color=discord.Color.blue()
                    )
                if len(command.aliases) > 1:
                    halp.add_field(
                        name='**Tambien llamado:**',
                        value=' / '.join(command.aliases),
                        inline=False
                    )
                if command.usage:
                    halp.add_field(
                        name='**Como lo uso?**',
                        value='```' + command.usage + '```',
                        inline=False
                    )
                if command.help:
                    halp.add_field(
                        name='**Que hace?**',
                        value=command.description,
                        inline=False
                    )
                if command.description:
                    halp.add_field(
                        name='**Ejemplo(s):**',
                        value=command.help,
                        inline=False
                    )
                return await ctx.send(embed=halp)

        halp=discord.Embed(
            title='Lo siento...'.format(ctx),
            description='''No existe ninguna categoria o comando llamado {}.
             **Prueba .help** para ver todos los comandos disponibles para ti'''.format(' '.join(nombre)),
            color=discord.Color.red()
        )
        return await ctx.send(embed=halp)

        
def setup(bot):
    bot.add_cog(help_commands(bot))