import discord
from discord.ext import commands
from ..classes.rol_class import FisRol
from ..classes.user_class import FisUser
from ..classes.display_class import Display
from ..classes.bot_class import context_is_admin


class custom_roles(
    commands.Cog,
    name='Roles'
    ):
    ''''''

    def __init__(self, bot):
        self.bot = bot


    def _help_embed(self, *, ctx) -> discord.Embed:
        '''Devuelve un `discord.Embed` con los roles disponibles por subida de nivel ordenados'''

        rol_list = FisRol().database.get_all_roles()

        frase = ''
        while rol_list:
            rol = rol_list.pop()
            disc_rol = ctx.guild.get_role(rol.id)
            if disc_rol and rol.level > 0:
                frase += f"\n{disc_rol.mention} -> Desbloqueado al nivel {rol.level}"

        roles=discord.Embed(
            title='Roles:',
            description='Estos son los roles disponibles por subida de nivel:' +  frase,
            color=discord.Color.purple()
        )
        
        return roles
        


    @commands.group(
        pass_context=True, 
        name='role',
        aliases=['roles', 'rol'],
        help='''¿Quieres ver los roles disponibles por subida de nivel? ```.roles```
        ¿Quieres crear un rol nuevo? ```.role create```
        ¿Quieres añadir un rol existente a la base de datos? ```.role add <role_mention>```
        ¿Quieres modificar un rol existente? ```.role modify <role_mention>```
        ¿Quieres eliminar un rol de la base de datos? ```.role delete <role_mention>```
        ''',
        brief='''.help role para mas informacion''',
        description='''Permite acceder al resto de comandos relacionados con los roles:
        ```
        subscribe:      Subscribirse a una asignatura
        unsubscribe:    Desubscribirse a una asignatura
        info:           Muestra informacion del rol
        create:         Crea un rol personalizado
        add:            Añade un rol a los roles personalizados
        delete:         Modifica un rol personalizado
        ```''',
        usage='.role <subcommand>'
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
        usage='.role create',
        checks=[context_is_admin]
    )
    async def _create(self, ctx):
        
        await FisRol().init_and_discord(ctx)


    @_roles.command(
        pass_context=True,
        aliases=['añadir'],
        help='''¿Quieres añadir el rol @Palos a los roles personalizados? ```.rol add @Palos```''',
        brief='''Añade un rol a los roles personalizados''',
        description='''Añade un rol existente a la base de datos y le asigna un nivel requerido para obtenerlo.
        Tambien permite añadirle descripcion y privilegios''',
        usage='.role add <rol_mentions>',
        check=[context_is_admin]
    )
    async def add(self, ctx):
        
        disc_rol = ctx.message.role_mentions[0]
        rol = FisRol.init_from_discord(ctx, disc_rol)
        await ctx.message.delete()
        if rol:
            await rol.modify()
        

    @_roles.command(
        pass_context=True,
        aliases=['mod'],
        help='''¿Quieres modificar el rol @Mods? ```.no puedes listillo```
        ¿Quieres modificar el rol @Escuderos de Juan Pablo? ```.rol modify @Escuderos de Juan Pablo```
        ''',
        brief='''Modifica un rol personalizado''',
        description='''Modifica un rol existente en la base de datos a traves de una sencilla interfaz. 
        Permite modificar nivel requerido, descripcion y privilegios''',
        usage='.role modify <rol_mention>',
        check=[context_is_admin]
    )
    async def modify(self, ctx):

        disc_rol = ctx.message.role_mentions[0]
        rol = FisRol.init_from_discord(ctx, disc_rol)
        await ctx.message.delete()
        if rol:
            await rol.modify()

    
    @_roles.command(
        pass_context=True,
        aliases=['dar', 'give'],
        help='''¿Quieres recibir notificaciones sobre Termodinamica? ```.role subscribe <@&753362848851165185>```''',
        brief='''Subscribirse a una asignatura''',
        description='''Permite subscribirse a las notificaciones sobre esa asignatura: 
        cada vez que se publique una noticia sobre ella te llegara una notificacion''',
        usage='.role subscribe <rol_mention> [-u [member_mention]]'
    )
    async def subscribe(self, ctx, **kargs):

        

        disc_rol = ctx.message.role_mentions[0]
        if '-u' in kargs and context_is_admin(ctx):
            user = FisUser.init_with_member(ctx.message.mentions[0])
        else:
            user = FisUser.init_with_member(ctx.author)
        await ctx.message.delete()

        if disc_rol:

            from ..database.roles import RolesDB
            rol = RolesDB().get_rol_id(disc_rol.id)
            rol.init_display(ctx)

            if rol.level < user.level:
                await rol.give_to(user)


    @_roles.command(
        pass_context=True,
        aliases=['quitar', 'drop'],
        help='''¿Quieres dejar de recibir notificaciones de la asignatura Termodinamica? ```.role unsubscribe <@&753362848851165185>```''',
        brief='''Desubscribirse de una asignatura''',
        description='''Te desubscribe de una asignatura: no recibiras mas notificaciones cuando haya noticias sobre ella''',
        usage='.role unsubscribe <rol_mention> [-u [member_mention]]'
    )
    async def unsubscribe(self, ctx, **kargs):

        disc_rol = ctx.message.role_mentions[0]
        if '-u' in kargs and context_is_admin(ctx):
            user = FisUser.init_with_member(ctx.message.mentions[0])
        else:
            user = FisUser.init_with_member(ctx.author)
        await ctx.message.delete()

        if disc_rol:

            from ..database.roles import RolesDB
            rol = RolesDB().get_rol_id(disc_rol.id)
            rol.init_display(ctx)

            if rol.level < user.level:
                await rol.remove_from(user)

    
    @_roles.command(
        pass_context=True,
        aliases=['help', 'h'],
        help='''¿Quieres informacion sobre el rol @Termodinamica? ```.role info <@&753362848851165185>```''',
        brief='''Muestra la informacion de un rol''',
        description='''Muestra la informacion sobre el rol especificado: 
        el nivel requerido para obtenerlo, privilegios y descripcion''',
        usage='.role info <rol_mention> [-dm [member_mention]]'
    )
    async def info(self, ctx, **kargs):

        disc_rol = ctx.message.role_mentions[0]
        if '-dm' in kargs and context_is_admin(ctx):
            with ctx.message.mentions[0] as user:
                channel = user.dm_channel
                if not channel:
                    channel = await user.create_dm()
        else:
            channel = ctx.channel
        if disc_rol:

            from ..database.roles import RolesDB
            rol = RolesDB().get_rol_id(disc_rol.id)
            rol.init_display(ctx)
            embed = await rol.embed_show()

            await channel.send(embed=embed)


    @_roles.command(
        pass_context=True,
        aliases=['remove', 'eliminar'],
        help='''¿Quieres modificar el rol @Mods? ```.no puedes listillo```
        ¿Quieres modificar el rol @Escuderos de Juan Pablo? ```.rol modify @Escuderos de Juan Pablo```
        ''',
        brief='''Modifica un rol personalizado''',
        description='''Modifica un rol existente en la base de datos a traves de una sencilla interfaz. 
        Permite modificar nivel requerido, descripcion y privilegios''',
        usage='.role info <rol_mention>',
        check=[context_is_admin]
    )
    async def delete(self, ctx):

        disc_rol = ctx.message.role_mentions[0]
        if disc_rol:
            try:
                await disc_rol.delete()
            except:
                pass
            else:
                from ..database.roles import RolesDB
                rol = RolesDB().get_rol_id(disc_rol.id)
                rol.database.del_rol(rol)
        await ctx.message.delete()


    @commands.command(
        pass_context=True,
        hidden=True
    )
    async def no(self, ctx, puedes, listillo):

        if puedes == 'puedes' and listillo == 'listillo':
            await ctx.send(f"Ssssh, me estas retando {ctx.author.mention}? Que soy admin colega... que te baneo")