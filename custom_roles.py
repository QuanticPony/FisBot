import discord
from discord.ext import commands

class custom_roles(
    commands.Cog,
    name='Roles'
    ):

    def __init__(self, bot):
        self.bot = bot


    def __help_embed(self, ctx) -> discord.Embed:
        ayuda=discord.Embed(
            title='Roles:',
            description='Estos son los roles disponibles por subida de nivel:',
            color=discord.Color.purple()
        )
        nivel = 0
        for rol in ctx.guild.roles:
            if not rol.permissions.manage_roles:
                ayuda.add_field(
                    name='{.mention}'.format(rol),
                    value='Desbloqueado al nivel {0}'.format(nivel),
                    inline=False
                )
                nivel += 1
        return ayuda
        


    @commands.group(
        pass_context=True, 
        name='rol',
        aliases=['roles'],
        help='''
        
        ''',
        brief='''Opera conjuntos de comandos''',
        description='''Permite modificar los roles existentes: crear, borrar, renombrar y actualizarlos''',
        usage='.rol <subcommand>'
    )
    async def _roles(self, context):
        if context.invoked_subcommand is None:
            await context.send(embed=custom_roles._help_embed(context))

    @_roles.group(
        pass_context=True,
        name='create',
        aliases=['c'],
        brief='Crea un nuevo rol con permisos personalizados',
        description='Crea un rol ',
        help='''C''',
    )
    async def _create(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Debes especificar el tipo de permisos, si quieres consultarlos prueba: ```.help rol create```')

    @_roles._create.command(
        pass_context=True,
        name='general',
        aliases=['g'],
        brief='Crea un rol'
    )
    async def _general(self, ctx, *, name):
        discord.Permissions


    
      