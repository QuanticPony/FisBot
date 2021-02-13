import discord
from discord.ext import commands
from .. import context_is_admin
from ..classes.user_class import FisUser
from ..classes.achievements_class import Achievements
from ..database.users import UsersDB

class users_cog(
    commands.Cog,
    name='Usuarios'
    ):

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
        pass_context=True, 
        aliases=['nivel','lvl'],
        help='''¿Quiere ver tu nivel? ```.level```
        ¿Quieres ver el nivel de <@730713148977578024>? ```.level @FisBot```''',
        brief='''Muestra nivel y experiencia''',
        description='''Muestra el nivel y la experiencia del autor del mensaje.
        En el caso de mencionar a alguien muestra su informacion''',
        usage='.level [member|s]'
    )
    async def level(self, ctx):

        embeds_list = []
        if not ctx.message.mentions:

            user = FisUser.convert_from_database(UsersDB.get_user, args=ctx.author.id)
            if not user:
                UsersDB.add_user(FisUser(ctx.author.id, name=ctx.author.name))
                user = FisUser.convert_from_database(UsersDB.get_user, args=ctx.author.id)

            if ctx.author.nick != user.name:
                user.name = ctx.author.nick
                UsersDB.update_user(user)

            await user.init_display(ctx)
            embeds_list.append(await user.embed_show())

        else:
            for user in ctx.message.mentions:

                user = FisUser.convert_from_database(UsersDB.get_user, args=user.id)

                if not user:
                    UsersDB.add_user(FisUser(user.id))
                    return
                    
                await user.init_display(ctx)
                embeds_list.append(await user.embed_show())

            await ctx.message.delete()

        for embed in embeds_list:
            await ctx.send(embed=embed)

        
    @commands.command(

    )
    async def colour(self, context, r, g, b):

        ach = Achievements.get_achievement(context.author)
        ach.set_color(r, g, b)
        await context.message.add_reaction("✔️")

    @commands.group(
        pass_context=True,
        hidden=True,
        name='user',
        aliases=['usuario'],
        brief='Permite modificar la base de datos de los usuarios',
        description='''Permite acceder a los comandos de modificacion y eliminacion de usuarios en la base de datos.
        Los subcomandos disponibles son:
        ```
        modify: <ADMIN> Modifica un usuario
        delete: <ADMIN> Elimina un usuario
        ```''',
        usage='.user <subcommand> <user_mention>',
        checks=[context_is_admin]
    )
    async def _user(self, ctx):
        pass

    @_user.command(
        hidden=True,
        pass_context=True,
        checks=[context_is_admin]
    )
    async def main_update(self, ctx):

        members = ctx.guild.members
        for member in members:
            UsersDB.update_user(await FisUser.init_with_member(member))

        await ctx.message.add_reaction("✔️")


    @_user.command(
        hidden=True,
        pass_context=True,
        checks=[context_is_admin]
    )
    async def main_reset(self, ctx):
        members = ctx.guild.members
        for member in members:
            user = await FisUser.init_with_member(member)
            user.level = 0
            user.xp = 0
            UsersDB.update_user(user)

        await ctx.message.add_reaction("✔️")

    @_user.command(
        pass_context=True,
        name='modify',
        aliases=['mod'],
        help='''¿Quieres modificar los atributos de @Jose?```.user modify @Jose```''',
        description='''Permite modificar nivel, experiencia, karma, y nombre de un usuario. Evidentemente si eres administrador''',
        brief='''Modifica un usuario en la base de datos''',
        usage='.user modify <user_mention>',
        checks=[context_is_admin]
    )
    async def _modify(self, ctx):

        disc_user = ctx.message.mentions
        if disc_user:
            disc_user = disc_user[0]
        
        user = await FisUser.init_with_member(disc_user, context=ctx)
        await ctx.message.delete()
        await user.modify()


    @_user.command(
        pass_context=True,
        name='delete',
        aliases=['del'],
        help='''¿Quiers borrar a @Pablo porque se ha ido del servidor? ```.user delete @Pablo```''',
        description='''**No usar este comando sin permiso previo** \nElimina al usuario mencionado de la base de datos''',
        brief='''Elimina un usuario de la base de datos''',
        usage='.user delete <user_mention>',
        checks=[context_is_admin]
    )
    async def _delete(self, ctx):

        disc_user = ctx.message.mentions
        if disc_user:
            disc_user = disc_user[0]
        
        user = await FisUser.init_with_member(disc_user, context=ctx)
        await ctx.message.delete()
        await user.delete()


    @commands.group(
        pass_context=True,
        name='karma',
        aliases=['k'],
        help='''¿Quieres ver tu karma? ```.karma```
        ¿Quieres ver el karma de @Victor? ```.karma @Victor```''',
        brief='''Karma de un usuario''',
        description='''Te muestra la informacion del usuario, igual que el comando ```.level```
        Los subcomandos disponibles son:
        ```
        rank muestra el top karma
        ```''',
        usage='.karma [user/s_mention/s]'
    )
    async def _karma(self, ctx):

        if not ctx.invoked_subcommand:
            await ctx.send('**Uso:** Para dar karma a alguien solo tienes que reaccionar con ⬆️ en un mensaje suyo. Para quitar ⬇️')
            await self.level(ctx)


    @_karma.command(
        pass_context=True,
        name='rank',
        aliases=['top','list','t'],
        help='''¿Quieres ver quién tiene más karma? ```.karma rank ```''',
        description='''Muestra una lista de los usuarios ordenados según su karma''',
        brief='''ranking del karma''',
        usage='.karma rank',
    )
    async def rank(self, ctx):
        
        lista = FisUser.convert_from_database(UsersDB.get_all_users)

        frase = []

        lista.sort(key = lambda memb : memb.karma)
        lista.reverse()

        check = False
        for i, memb in enumerate(lista, start=1):
            if i <= 10:
                if memb.id == ctx.author.id:
                    check = True
                    frase.append(f"**{i} - {memb.name}: {memb.karma}**")
                else:
                    frase.append(f"*{i} - {memb.name}*: {memb.karma}")
            else:
                if not check:
                    user = await FisUser.init_with_member(ctx.author)
                    frase.append('...')
                    frase.append(f"**{lista.index(user)} - {user.name}: {user.karma}**")
                break
    

        embed= discord.Embed(
            title='Ranking karma points',
            description='Estos son l@s Físic@s que tienen más karma (fijo que son buena gente)\n' + '\n'.join(frase),
            color=discord.Color.orange()
        )

        await ctx.send(embed=embed) 

    @commands.command(
        pass_context=True,
        hidden=True
    )
    async def no(self, ctx, puedes, listillo):

        if puedes == 'puedes' and listillo == 'listillo':
            await ctx.send(f"Ssssh, me estas retando {ctx.author.mention}? Que soy admin colega... que te baneo")


    @commands.command(
        pass_context=True, 
        brief='''Te da 3.14 de experiencia''',
        description='''pi matematicos, pi fisicos, pi ingenieros, pi de letras, pi pi''',
        usage='.pi [modo]'
    )
    async def pi(self, context, *mode):
        types = {'matematicos': 'π',
        'ingenieros': '5',
        'fisicos': '3.14',
        'pi': 'Que infantil...',
        'de letras': '''Se reflejaba en el agua
el pájaro confundido,
levantaba la cabeza
que asomaba desde el nido.

Eh, amigo - le gritó -
¿Vienes a volar conmigo?
Parecemos muy iguales,
seremos buenos amigos.
He descargado este poema
para escribir Pi (o) pi (o)

Pájaro escucha, -insistió-
Te pareces mucho a mí,
tienes las plumas verdosas
y el pico color añil.

Pero el ave sin moverse 
miraba sin contestar,
y el pajarito en el árbol
se empezó a desesperar.

Oyes, pájaro antipático
¿Es que acaso no me ves?
aquí arriba -gritó fuerte-
en el nido del ciprés.

Pero el reflejo del agua
no se dignó a contestar,
y el del árbol enfadado
protestando echó a volar. 
(Lo he copiado de internet, evidentemente)'''}

        if not mode:
            await context.send('''3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912''')
            return 
        mode = ' '.join(mode)
        for key in types.keys():
            if mode in key:
                await context.send(types[key])
                return


    @commands.command(
        pass_context=True, 
        brief='''Convierne grados a radianes''',
        description='''Hace el cambio que todos necesitamos; pero que solo David Perez no hace''',
        usage='.david [numero]'
    )
    async def david(self, context, *, number):
        if number and number.isnumeric():
            await context.send(f"{float(number)}º son {float(number)/180:.3}π magnificos radianes")
        else:
            await context.send('''David Perez es un miembro de FisCord conocido por su aprecio incondicional al sistema sexagesimal para la medida de angulos''')
