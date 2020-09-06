import discord
from discord.ext import commands
from ..classes.rol_class import FisRol
from ..classes.display_class import Display
from ..classes.bot_class import context_is_admin


class custom_roles(
    commands.Cog,
    name='Roles'
    ):

    def __init__(self, bot):
        self.bot = bot


    def _help_embed(self, *, ctx) -> discord.Embed:
        '''Devuelve un `discord.Embed` con los roles disponibles por subida de nivel ordenados'''

        rol_list = FisRol().database.get_all_roles()

        frase = ''
        while rol_list:
            rol = rol_list.pop()
            disc_rol = ctx.guild.get_role(rol.rol_id)
            if disc_rol:
                frase += f"\n{disc_rol.mention} -> Desbloqueado al nivel {rol.level}"

        roles=discord.Embed(
            title='Roles:',
            description='Estos son los roles disponibles por subida de nivel:' +  frase,
            color=discord.Color.purple()
        )
        
        return roles
        


    @commands.group(
        pass_context=True, 
        name='rol',
        aliases=['roles'],
        help='''¿Quieres ver los roles disponibles por subida de nivel? ```.rol```
        ¿Quieres crear un rol nuevo? ```.rol create <rol_name>```
        ¿Quieres añadir un rol existente a la base de datos?
        
        ''',
        brief='''Opera conjuntos de comandos''',
        description='''Permite modificar los roles existentes: crear, borrar, renombrar y actualizarlos''',
        usage='.rol <subcommand>'
    )
    async def _roles(self, context):
        if context.invoked_subcommand is None:
            await context.send(embed=self._help_embed(ctx=context))

    @_roles.command(
        pass_context=True,
        name='create',
        aliases=['c'],
        brief='Crea un rol personalizado',
        description='Crea un nuevo rol con permisos \"generales\" y lo incluye en la base de datos',
        help='''¿Quieres crear un rol? ```.rol create```''',
        usage='.rol create <rol_name>',
        checks=[context_is_admin]
    )
    async def _create(self, ctx):
        
        disc_rol = await FisRol().create_discord_obj(ctx, 'None')
        rol = FisRol(rol_id=disc_rol.id)
        display = Display(rol, ctx, role=True)
        display.create()


    @_roles.command(
        pass_context=True,
        aliases=['roles'],
        help='''¿Quieres añadir el rol @Palos a los roles personalizados? ```.rol add @Palos```''',
        brief='''Añade un rol a los roles personalizados''',
        description='''Añade un rol existente a la base de datos y le asigna un nivel requerido para obtenerlo.
        Tambien permite añadirle descripcion y privilegios''',
        usage='.rol add <rol_mentions>'
    )
    async def add(self, ctx, *args):
        
        disc_rol_list = ctx.message.role_mentions
        if len(disc_rol_list) == 1:
            disc_rol = disc_rol_list.pop()

            new_rol = FisRol(rol_id=disc_rol.id)
            await new_rol.modify(ctx)
            new_rol.database.add_rol(new_rol)
            await ctx.message.add_reaction('✅')

        else:
            if not args:
                return
            await ctx.send('Estoy diseñado para añadir roles de uno en uno, lo siento')
        

    @_roles.command(
        pass_context=True,
        aliases=['mod'],
        help='''¿Quieres modificar el rol @Mods? ```.no puedes listillo```
        ¿Quieres modificar el rol @Escuderos de Juan Pablo? ```.rol modify @Escuderos de Juan Pablo```
        ''',
        brief='''Modifica un rol personalizado''',
        description='''Modifica un rol existente en la base de datos a traves de una sencilla interfaz. 
        Permite modificar nivel requerido, descripcion y privilegios''',
        usage='.rol modify <rol_id/rol_mention>'
    )
    async def modify(self, ctx, *, args):

        disc_rol_list = ctx.message.role_mentions
        if len(disc_rol_list) == 1:
            disc_rol = disc_rol_list.pop()
            rol = FisRol().database.get_rol_id(disc_rol.id)
            await rol.modify(ctx)

        else:
            disc_rol = ctx.guild.get_role(int(args))
            if disc_rol:
                rol = FisRol().database.get_rol_id(disc_rol.id)
                if await rol.modify(ctx):
                    await ctx.message.add_reaction('✅')
                else:
                    await ctx.message.add_reaction('❌')