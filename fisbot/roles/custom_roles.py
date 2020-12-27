import discord
from discord.ext import commands
from ..classes.rol_class import FisRol
from ..classes.user_class import FisUser
from ..classes.display_class import Display
from ..classes.bot_class import context_is_admin
from ..database.roles import RolesDB


class custom_roles_cog(
    commands.Cog,
    name='Roles'
    ):
    '''Conjunto de comandos relacionados con los roles personalizados del servidor.
    Para mas informacion pruebe: ```.help role```'''

    def __init__(self, bot):
        self.bot = bot


    def _help_embed(self, ctx, *, mode=None) -> discord.Embed:
        
        if not mode:
            '''Devuelve un `discord.Embed` con los roles disponibles por subida de nivel ordenados'''

            rol_list = FisRol().database.get_all_guild_roles(ctx.guild.id)

            frase = ''
            while rol_list:
                rol = rol_list.pop()
                disc_rol = ctx.guild.get_role(rol.id)
                if disc_rol and rol.level > 0:
                    frase += f"\n{disc_rol.mention} -> Desbloqueado al nivel {rol.level}"

            roles=discord.Embed(
                title='Roles de niveles:',
                description='Estos son los roles disponibles por subida de nivel:' +  frase,
                color=discord.Color.purple()
            )
            return roles

        if mode:
            '''Devuelve un `discord.Embed` con los roles sobre asignaturas (lvl < 0)'''
            try:
                rol_list = FisRol().database.get_all_guild_roles(ctx.guild.id)
            except:
                return discord.Embed(
                    title='Hubo un error', 
                    description='Así que me tomo un melocotón\n lol',
                    color=discord.Color.red())
                    
            frase = ''
            while rol_list:
                rol = rol_list.pop()
                disc_rol = ctx.guild.get_role(rol.id)
                if disc_rol and rol.level < 0:
                    frase += f"\n{disc_rol.mention}"

            roles=discord.Embed(
                title='Roles de asignaturas:',
                description='Estos son los roles disponibles sobre asignaturas:' +  frase,
                color=discord.Color.purple()
            )
            return roles


    @commands.group(
        pass_context=True, 
        name='role',
        aliases=['roles', 'rol'],
        help='''¿Quieres ver los roles disponibles por subida de nivel? ```.roles```
        ¿Quieres ver las asignaturas existentes? ```.roles subjects```
        ¿Quieres recibir notificaciones sobre Termodinamica? ```.role subscribe <@&753362848851165185>```
        ¿Quieres dejar de recibir notificaciones sobre Termodinamica? ```.role unsubscribe <@&753362848851165185>```
        ¿Quieres informacion sobre el rol @Termodinamica? ```.role info <@&753362848851165185>```
        ''',
        brief='''Prefijo para acceder a comandos de roles''',
        description='''Permite acceder al resto de comandos relacionados con los roles:
        ```
        subscribe:      Subscribirse a una asignatura
        unsubscribe:    Desubscribirse a una asignatura
        info:           Muestra informacion del rol
        subjects:       Muestra las asignaturas disponibles
        create:         <Admin> Crea un rol personalizado
        add:            <Admin> Añade un rol existente
        modify:         <Admin> Modifica un rol personalizado
        delete:         <Admin> Elimina un rol personalizado
        ```''',
        usage='.role [subcommand] [args]'
    )
    async def _roles(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=self._help_embed(ctx))


    @_roles.command(
        pass_context=True,
        name='create',
        aliases=['c', 'crear'],
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
        aliases=['añadir', 'a'],
        help='''¿Quieres añadir el rol @Palos a los roles personalizados? ```.rol add @Palos```''',
        brief='''Añade un rol a los roles personalizados''',
        description='''Añade un rol existente a la base de datos y le asigna un nivel requerido para obtenerlo.
        Tambien permite añadirle descripcion y privilegios''',
        usage='.role add <rol_mention>',
        check=[context_is_admin]
    )
    async def add(self, ctx):
        
        disc_rol = ctx.message.role_mentions
        if disc_rol:
            disc_rol = disc_rol[0]
            rol = await FisRol.init_from_discord(ctx, disc_rol)
            if rol:
                await rol.modify()
            await ctx.message.delete()
        

    @_roles.command(
        pass_context=True,
        aliases=['mod','m'],
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

        disc_rol = ctx.message.role_mentions
        if disc_rol:
            disc_rol = disc_rol[0]
        else:
            return
        rol = await FisRol.init_from_discord(ctx, disc_rol)
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
        usage='.role subscribe [-year [school_year]] [-user [user_mention]] <rol_mention/s>'
    )
    async def subscribe(self, ctx, *args):

        subjects_list = ctx.message.role_mentions
        role_list = []

        if '-year' in args:
            year = subjects_list[subjects_list.index('-year') + 1]
            if year.isnumeric():
                role_list = RolesDB.get_roles(-abs(int(year)), guild_id=ctx.guild.id)
            else:
                return
        else:
            for subject in subjects_list:
                role_list.append(await FisRol.init_from_discord(ctx, subject))


        admin = '-u' in admin and context_is_admin(ctx)
        if admin:
            user = await FisUser.init_with_member(ctx.message.mentions[0])
        else:
            user = await FisUser.init_with_member(ctx.author)
        await ctx.message.delete()

        for role in role_list:
            if role.level < 0 or admin:
                await role.give_to(user)



    @_roles.command(
        pass_context=True,
        aliases=['quitar', 'drop'],
        help='''¿Quieres dejar de recibir notificaciones de la asignatura Termodinamica? ```.role unsubscribe <@&753362848851165185>```''',
        brief='''Desubscribirse de una asignatura''',
        description='''Te desubscribe de una asignatura: no recibiras mas notificaciones cuando haya noticias sobre ella''',
        usage='.role unsubscribe [-year [school_year]] <rol_mention> [-u [member_mention]]'
    )
    async def unsubscribe(self, ctx, *args):

        subjects_list = ctx.message.role_mentions
        role_list = []

        if '-year' in args:
            year = subjects_list[subjects_list.index('-year') + 1]
            if year.isnumeric():
                role_list = RolesDB.get_roles(-abs(int(year)), guild_id=ctx.guild.id)
            else:
                return
        else:
            for subject in subjects_list:
                role_list.append(await FisRol.init_from_discord(ctx, subject))


        admin = '-u' in admin and context_is_admin(ctx)
        if admin:
            user = await FisUser.init_with_member(ctx.message.mentions[0])
        else:
            user = await FisUser.init_with_member(ctx.author)
        await ctx.message.delete()

        for role in role_list:
            if role.level < 0 or admin:
                await role.remove_from(user)

    
    @_roles.command(
        pass_context=True,
        aliases=['help', 'h'],
        help='''¿Quieres informacion sobre el rol @Termodinamica? ```.role info <@&753362848851165185>```''',
        brief='''Muestra la informacion de un rol''',
        description='''Muestra la informacion sobre el rol especificado: 
        el nivel requerido para obtenerlo, privilegios y descripcion''',
        usage='.role info <rol_mention> [-dm [member_mention]]'
    )
    async def info(self, ctx, *args):

        disc_rol = ctx.message.role_mentions
        if disc_rol:
            disc_rol = disc_rol[0]
        else:
            return

        if '-dm' in args and context_is_admin(ctx):
            member = ctx.message.mentions[0]
            channel = member.dm_channel
            if not channel:
                channel = await member.create_dm()
        else:
            channel = ctx.channel
            
        if disc_rol:
            rol = await FisRol.init_from_discord(ctx, disc_rol)
            embed = await rol.embed_show()

            await channel.send(embed=embed)
            await ctx.message.delete()


    @_roles.command(
        pass_context=True,
        aliases=['d', 'remove', 'eliminar'],
        help='''¿Quieres modificar el rol @Mods? ```.no puedes listillo```
        ¿Quieres modificar el rol @Escuderos de Juan Pablo? ```.rol modify @Escuderos de Juan Pablo```
        ''',
        brief='''Modifica un rol personalizado''',
        description='''Modifica un rol existente en la base de datos a traves de una sencilla interfaz. 
        Permite modificar nivel requerido, descripcion y privilegios''',
        usage='.role delete <rol_mention>',
        check=[context_is_admin]
    )
    async def delete(self, ctx):

        disc_rols = ctx.message.role_mentions
        for disc_rol in disc_rols:
            try:
                await disc_rol.delete()
            except:
                pass
            else:
                RolesDB.del_rol(FisRol(rol_id=disc_rol.id))
        await ctx.message.delete()


    @commands.command(
        pass_context=True,
        aliases=['asignaturas'],
        brief='''Muestra los roles de asignaturas creados''',
        description='''Muestra los roles de asignaturas creados, disponibles para cualquier usuario con al menos nivel 1''',
        usage='.subjects',
        
    )
    async def subjects(self, ctx):

        await ctx.send(embed=self._help_embed(ctx, mode=1))


    @commands.command(
        pass_context=True,
        hidden=True
    )
    async def no(self, ctx, puedes, listillo):

        if puedes == 'puedes' and listillo == 'listillo':
            await ctx.send(f"Ssssh, me estas retando {ctx.author.mention}? Que soy admin colega... que te baneo")