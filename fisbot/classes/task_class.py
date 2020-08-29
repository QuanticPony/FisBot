import discord
import asyncio

class FisTask():
    def __init__(self, task_id=None, subject='', title='', description='', day=None, month=None, year=None, school_year = None, url=None):
        self._id = task_id
        self.subject = subject
        self.title = title
        self.description = description
        self.day = day
        self.month = month
        self.year = year
        self.school_year = school_year
        self.url = url

        from ..database.tasks import ProyectsDB
        self.database = ProyectsDB()


    def embed(self) -> discord.Embed:
        '''Devuelve un mensaje tipo `discord.Embed` que muestra la tarea'''

        task_embed = discord.Embed(
            title=f"**{self.school_year}º -> {self.subject}**",
            description=f"[**{self.title}**]({self.url})" if self.url else f"**{self.title}**",
            color=discord.Color.purple()
        )
        task_embed.add_field(
            name='Fecha:',
            value='{0.day}/{0.month}'.format(self) + ('/{0.year}'.format(self)) if self.year else '',
            inline=True
        )
        task_embed.add_field(
                name='Id:',
                value=f'**{self._id}**',
                inline=True
        )
        task_embed.add_field(
            name='**Descripcion:**',
            value=self.description if self.description else '*Sin especificar*',
            inline=False
        )
        task_embed.set_footer(text='Si cree necesaria alguna modificacion en este mensaje por favor pongase en contacto con algun moderador (@mods)')

        return task_embed

    async def modify(self, ctx):
        _atributes_dic = self.__dict__
        atributes_dic = _atributes_dic.copy()
        embed = discord.Embed(
            title=f"Modificar: {self.subject} ({self.school_year}º): {self.title}*",
            description='Selecciona el campo a modificar:',
            color=discord.Color.dark_orange()
        )
        atributes_dic.pop('_id')
        atributes_dic.pop('database')

        codepoint_start = 127462  # Letra A en unicode en emoji
        things_list = {f"{chr(i)}": v for i, v in enumerate(atributes_dic, start=codepoint_start)}

        for atrib in things_list:
            value = atributes_dic[things_list[atrib]]
            if not value: 
                value = 'None'
            embed.add_field(
                name=f"{atrib} - {things_list[atrib]}:",
                value=atributes_dic[things_list[atrib]],
                inline=False
                )

        message = await ctx.send(embed=embed)
        for i in range(len(things_list)):
            await message.add_reaction(chr(i+codepoint_start)) 
        await message.add_reaction("💾")

        def confirm_reaction(reaction, user):
            return user.id == ctx.message.author.id
        def confirm_message(response_msg):
            return response_msg.author.id == ctx.message.author.id

        async def ask_field() -> bool:
            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=15.0, check=confirm_reaction)
                if str(reaction.emoji) == '💾':
                    return False
                
            except asyncio.TimeoutError:
                await ctx.send('Se acabo el tiempo...')
                return False
            
            ask_message = await ctx.send(f"Introduce un nuevo {things_list[reaction.emoji]}:")

            try:
                response_msg = await ctx.bot.wait_for('message', timeout=60.0, check=confirm_message)
            except asyncio.TimeoutError:
                await ctx.send('Se acabo el tiempo...')
                return False
              
            setattr(self, things_list[reaction.emoji], response_msg.content)
            await response_msg.add_reaction("✅")
            return True


        while await ask_field():
            pass
        self.database.update_task(self)
        return

        

        
        
        

        
            
        
