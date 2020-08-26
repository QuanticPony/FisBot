import discord
import asyncio

class FisTask():
    def __init__(self, task_id=None, subject='', title='', description='', day=None, month=None, year=None):
        self.id = task_id
        self.subject = subject
        self.title = title
        self.description = description
        self.day = day
        self.month = month
        self.year = year

        from ..database.tasks import ProyectsDB
        self.database = ProyectsDB()


    def embed(self) -> discord.Embed:
        '''Crea un mensaje tipo discord.Embed que muestra la tarea'''

        task_embed = discord.Embed(
            title='**{0.subject}**: *{0.title}*'.format(self),
            description='Fecha: {0.day}/{0.month}'.format(self) + ('/{0.year}'.format(self)) if self.year else '',
            color=discord.Color.purple()
        )

        task_embed.add_field(
            name='**Descripcion:**',
            value=self.description if self.description else '*Sin especificar*',
            inline=False
        )

        task_embed.add_field(
                name='Id:',
                value='**{0.id}**'.format(self),
                inline=False
            )
        task_embed.set_footer(text='Si cree necesaria alguna modificacion en este mensaje por favor pongase en contacto con algun moderador (@mods)')

        return task_embed

    async def modify(self, ctx) -> discord.Embed:
        atributes_dic = self.__dict__

        embed = discord.Embed(
            title='Modificar: *{0.subject}: {0.title}*'.format(self),
            description='Selecciona el campo a modificar:',
            color=discord.Color.dark_orange()
        )
        atributes_dic.pop('id')
        atributes_dic.pop('database')

        codepoint_start = 127462  # Letra A en unicode en emoji
        #things_list = {chr(i): f"{chr(i)} - {atrib}" for i, atrib in enumerate(atributes_dic.keys(), start=codepoint_start)}
        things_list = {f"{chr(i)} - {v}:": f"{atributes_dic[v]}" for i, v in enumerate(atributes_dic, start=codepoint_start)}

        for atrib in things_list:
            embed.add_field(
                name=atrib,
                value=things_list[atrib],
                inline=False
                )

        message = await ctx.send( '@everyone',embed=embed)
        for i in range(len(things_list)):
            await message.add_reaction(chr(i+codepoint_start)) 
        return embed
        def confirm(reaction, user):
            return ctx.message.author == user
        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=confirm)
            
        except asyncio.TimeoutError:
            await message.delete()
        else:
            await ctx.message.channel.delete()
        
