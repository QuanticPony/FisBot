import discord
from discord.ext import commands
from ..classes.user_class import FisUser

class levels(
    commands.Cog,
    name='Niveles'
    ):

    def __init__(self, bot):
        self.bot = bot

    
    def show(self, ctx, user_id) -> discord.Embed:
        '''Crea un objeto `discord.Embed` que muestra la informacion relativa al usuario requerido'''
        dis_user = ctx.guild.get_member(int(user_id))
        fis_user = FisUser().database.get_user(user_id)
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
        aliases=['nivel','lvl'],
        help=f'''¿Quiere ver tu nivel? ```.level```
        ¿Quieres ver el nivel de <@730713148977578024>? ```.level @FisBot```''',
        brief='''Muestra nivel y experiencia''',
        description='''Muestra el nivel y la experiencia del autor del mensaje.
        En el caso de mencionar a alguien muestra su informacion''',
        usage='.level [member|s]'
    )
    async def level(self, ctx):
        embeds_list = []
        if not ctx.message.mentions:
            user = FisUser().database.get_user(ctx.author.id)
            if not user:
                user.database.add_user(user)
            embeds_list.append(self.show(ctx, user.id))

        else:
            for user in ctx.message.mentions:
                user = FisUser().database.get_user(user.id)
                if not user:
                    user.database.add_user(user)
                embeds_list.append(self.show(ctx, user.id))

        for embed in embeds_list:
            await ctx.send(f"{ctx.author.mention}", embed=embed)
        
    
            
