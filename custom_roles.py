import discord
import asyncio
from discord.ext import commands


"""En proceso, no usar"""

class custom_roles(
    commands.Cog,
    name='Roles'
    ):

    def __init__(self, bot):
        self.bot = bot


    def _roles_help_embed(self, ctx):
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
            pass


    
def setup(bot):
    bot.add_cog(custom_roles(bot))
      