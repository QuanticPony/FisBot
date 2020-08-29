import discord
from discord.ext import commands
from ..classes.bot_class import context_is_admin
from ..classes.rol_class import FisRol

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
            
        rol_list = FisRol().database.get_all_roles()

        while rol_list:
            rol = rol_list.pop()
            disc_rol = ctx.guild.get_rol(rol.rol_id)
            if disc_rol:
                ayuda.add_field(
                    name=f"{disc_rol.mention}",
                    value=f"Desbloqueado al nivel {rol.level}",
                    inline=False
                )
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

    @_roles.command(
        pass_context=True,
        name='create',
        aliases=['c'],
        brief='Crea un nuevo rol con permisos personalizados',
        description='Crea un rol ',
        help='''¿Quieres crear un rol? ```.rol create```''',
        checks=[context_is_admin]
    )
    async def _create(self, ctx, *, rol_name):
        pass


    @_roles.command(
        pass_context=True,
        brief='Hola'
    )
    async def add(self, ctx):
        
        disc_rol_list = ctx.message.role_mentions
        if len(disc_rol_list) == 1:
            disc_rol = disc_rol_list.pop()

            new_rol = FisRol(rol_id=disc_rol.id)
            await new_rol.modify(ctx)
            new_rol.database.add_rol(new_rol)
            await ctx.message.add_reaction('✅')

        else:
            await ctx.send('Estoy diseñado para añadir roles de uno en uno, lo siento')
        
        


