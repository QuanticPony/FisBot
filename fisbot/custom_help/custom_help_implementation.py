import discord
from discord.ext import commands
from .. import context_is_admin


async def custom_help_implementation_all(bot, ctx):
    halp=discord.Embed(
            title='.help', 
            description='Estos son todos los comandos. Probablemente no tengas permisos para usar todos:'.format(ctx), 
            color=discord.Color.green()
        )
    admin = context_is_admin(ctx)
    for cog in bot.cogs.values():
        commands_desc = ''
        for x in cog.get_commands():
            if not x.hidden or admin:
                commands_desc += ('{0: <15} {1}'.format(x.name,x.brief) + '\n')

        if commands_desc:
            halp.add_field(
                name=cog.qualified_name,
                value=commands_desc,
                inline=False
            )
    return await ctx.send(embed=halp)


async def custom_help_implementation_general(bot, ctx):
    halp=discord.Embed(
            title='.help', 
            description='Estos son los comandos disponibles para {0.author.mention}:'.format(ctx), 
            color=discord.Color.green()
        )

    admin = context_is_admin(ctx)
    for cog in bot.cogs.values():
        commands_desc = ''
        for x in cog.get_commands():
            if await x.can_run(ctx) and (not x.hidden or admin):
                commands_desc += ('{0: <15} {1}'.format(x.name,x.brief) + '\n')

        if commands_desc:
            halp.add_field(
                name=cog.qualified_name,
                value=commands_desc,
                inline=False
            )
    return await ctx.send(embed=halp)

async def custom_help_implementation_command(bot, ctx, nombre):
    cog = bot.get_cog(nombre)
    # Se da categoria
    admin = context_is_admin(ctx)
    if cog:
        commands_desc = ''
        for x in cog.get_commands():
            if await x.can_run(ctx) and (not x.hidden or admin):
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


    command = bot.get_command(nombre)
    # Se da comando
    if command:
        halp=discord.Embed(
                title='**{0.cog.qualified_name}**: *.{0.name}*'.format(command), 
                description=command.brief,
                color=discord.Color.blue()
            )
        if len(command.aliases) >= 1:
            
            if len(command.aliases) ==1:
                value = command.aliases[0]
                
            else:
                value =' / '.join(command.aliases)
            
            halp.add_field(
                name='**Tambien llamado:**',
                value=value,
                inline=False
            )
        if command.usage:
            halp.add_field(
                name='**Como lo uso?**',
                value='```' + command.usage + '```',
                inline=False
            )
        if command.description:
            halp.add_field(
                name='**Que hace?**',
                value=command.description,
                inline=False
            )
        if command.help:
            halp.add_field(
                name='**Ejemplo(s):**',
                value=command.help,
                inline=False
            )
        return await ctx.send(embed=halp)

    halp=discord.Embed(
        title='Lo siento...'.format(ctx),
        description='''No existe ninguna categoria o comando llamado {}.
         **Prueba .help** para ver todos los comandos disponibles para ti'''.format(nombre),
        color=discord.Color.red()
    )
    return await ctx.send(embed=halp)