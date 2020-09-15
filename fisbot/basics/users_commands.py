import discord
from discord.ext import commands
from ..classes.user_class import FisUser
from ..database.users import UsersDB

class users_cog(
    commands.Cog,
    name='Usuarios'
    ):

    def __init__(self, bot):
        self.bot = bot
    
    def show(self, ctx, *, user_id=None, user=None) -> discord.Embed:
        '''Crea un objeto `discord.Embed` que muestra la informacion relativa al usuario requerido'''

        if ctx.guild and user_id:
            dis_user = ctx.guild.get_member(int(user_id))
        if user:
            dis_user = user
        
        fis_user = FisUser().database.get_user(dis_user.id)
        fis_user.name = dis_user.nick
        fis_user.database.update_user(fis_user)
        embed = discord.Embed(
            title = fis_user.name,
            description = f'Nombre en discord: {dis_user.name}',
            color = discord.Color.from_rgb(0,179,255)
        )
        embed.add_field(
            name='Nivel',
            value=fis_user.level,
            inline=True
            )
        embed.add_field(
            name='Experiencia',
            value=f"{fis_user.xp}/{fis_user.xp_to_lvl_up()}",
            inline=True
        )
        embed.set_thumbnail(url=str(dis_user.avatar_url_as(size=128)))
        embed.set_footer(text='Si cree que el nivel no se corresponde con lo que se merece, participe mas')
        return embed

    @commands.command(
        pass_context=True, 
        aliases=['nivel','lvl','karma'],
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

            user = UsersDB.get_user(ctx.author.id)

            if not user:
                UsersDB.add_user(user)
            await user.init_display(ctx)
            embeds_list.append(await user.embed_show())

        else:
            for user in ctx.message.mentions:

                user = UsersDB.get_user(user.id)

                if not user:
                    UsersDB.add_user(user)
                await user.init_display(ctx)
                embeds_list.append(await user.embed_show())

        for embed in embeds_list:
            await ctx.send(f"{ctx.author.mention}", embed=embed)

    @commands.group(
        pass_context=True,
        hidden=True,
        name='user',
        aliases=['usuario'],
        brief='Permite modificar la base de datos de los usuarios',

    )
    async def _users(self, ctx):
         if not ctx.invoked_subcommand:
            await self.level(ctx)

    @_users.command(
        pass_context=True,
        name='modify',
        aliases=['mod'],
        help='''''',
        description='''''',
        brief='''''',
        usage='.user modify'
    )
    async def _modify(self, ctx):...
        



    @commands.group(
        pass_context=True,
        name='',
        aliases=[''],
        help='''¿? ```.```
        ¿? ```.```''',
        brief='''permite ver el karma de un usuario''',
        description='''''',
        usage=''
    )
    async def _karma(self, ctx):
        if not ctx.invoked_subcommand:
            await self.level(ctx)
        
  
    @_karma.group(
        pass_context=True,
        name='',
        aliases=[''],
        help='''¿? ```.```
        ¿? ```.```''',
        brief='''''',
        description='''''',
        usage=''
    )
    async def up(self, ctx):
        if not ctx.message.mentions:

            user = UsersDB.get_user(ctx.author.id)

            if not user:
                UsersDB.add_user(user)

            

        else:
            for user in ctx.message.mentions:

                user = UsersDB.get_user(user.id)

                if not user:
                    UsersDB.add_user(user)
                
    @_karma.group(
        pass_context=True,
        name='',
        aliases=[''],
        help='''¿? ```.```
        ¿? ```.```''',
        brief='''''',
        description='''''',
        usage=''
    )
    async def _down(self, ctx):...