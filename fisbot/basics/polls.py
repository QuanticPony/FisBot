import discord
import asyncio
import random
from discord.ext import commands
from ..classes.bot_class import context_is_admin


class Poll():
    CODE_POINT = 127462
    def __init__(self, title='Titulo', description='Descripcion', values=['Elemento 1']):
        self.index = 0
        self.options = {
            '🟫': ['Titulo', title],
            '🟩': ['Descripcion', description]
        }
        self.options.update({f"{chr(self.index + self.CODE_POINT)}": [v, 'Null'] for self.index, v in enumerate(values)})


    def add_element(self, value):
        '''Añade un nuevo elemento al objeto Poll'''

        self.index += 1
        element = [f'Elemento {self.index}', value]
        self.options[chr(self.index + self.CODE_POINT)] = element
        


    def mod_element(self, key, value):
        '''Modifica un elemento del objeto Poll'''

        self.options[key][1] = value


    def del_element(self, key) -> bool:
        '''Borra un campo del objeto Poll y devuelve `True`. Si ese campo es el titulo o la descripcion, devuelve `False`'''

        if key == '🟫' or '🟩':
            return False
        else:
            self.options.pop(key)
            self.index -= 1
            return True
    
    def return_values(self) -> dict:
        '''Devuelve los elementos de la encuesta en un diccionario cuya key es un `Emoji` y el value es la opcion'''

        dict_copy = self.options.copy()
        dict_copy.pop('🟫')
        dict_copy.pop('🟩')
        return dict_copy





class poll_cog(
    commands.Cog, 
    name='Encuestas',
    ):
    '''Comandos para realizar encuestas. Pasos para realizar una: escriba ```.poll``` donde quiere que aparezca la encuesta.
    Cambia los campos de la encuesta por mensajes privados. Cuando este acabado pulsa 💾'''

    def __init__(self, bot):
        self.bot = bot


    async def create_poll(self, ctx) -> (discord.Embed, list):
        '''Crea una encuesta a traves de un dialogo por mensajes privados. Devuelve una `tupla` cuyos 
        elementos son el `embed` y una `lista` de las opciones respectivamente'''

        poll = Poll()
        channel = ctx.author.dm_channel
        if not channel:
            channel = await ctx.author.create_dm()


        new_poll = discord.Embed(
            title='Nueva encuesta:',
            description='❎ Añade una opcion y ❌ borra el campo con el emoticono que envies en tu siguiente mensaje. Selecciona el campo a modificar:',
            color=discord.Color.blurple()
        )

        for element in poll.options:
            new_poll.add_field(
                name=f"{element} - {poll.options[element][0]}",
                value=f"{poll.options[element][1]}",
                inline=False
            )

        config_message = await channel.send(embed=new_poll)

        for i in poll.options:
            await config_message.add_reaction(i) 
        await config_message.add_reaction("❎")
        await config_message.add_reaction("❌")
        await config_message.add_reaction("💾")



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
                await channel.send('Se acabo el tiempo...')
                return False

            ask_message = await channel.send('Introduce el nuevo valor:')
            try:
                response_msg = await ctx.bot.wait_for('message', timeout=120.0, check=confirm_message)
            except asyncio.TimeoutError:
                await channel.send('Se acabo el tiempo...')
                return False

            if reaction.emoji == '❎':
                poll.add_element(response_msg.content)
            elif reaction.emoji == '❌':
                if response_msg.content in poll.keys():
                    poll.del_element(response_msg.content)
                else:
                    channel.send('No existe ese campo')
            else:
                poll.mod_element(reaction.emoji, response_msg.content)
            
            await ask_message.delete()
            return True


        while await ask_field():
            new_poll.clear_fields()
            for element in poll.options:
                new_poll.add_field(
                    name=f"{element} - {poll.options[element][0]}",
                    value=f"{poll.options[element][1]}",
                    inline=False
            )
            await config_message.edit(embed=new_poll)


        final_poll = discord.Embed(
            title=poll.options['🟫'][1],
            description=poll.options['🟩'][1],
            color=discord.Color.blurple()
        )
        elements_dic = poll.return_values()

        frase = ''
        for i in elements_dic:
            frase += f"{i} - {elements_dic[i][1]}\n"

        final_poll.add_field(
            name='Opciones:',
            value=frase,
            inline=False
            )
        return (final_poll, list(elements_dic.keys()))



    @commands.command(
        pass_context=True, 
        aliases=['encuesta','p'],
        help='''¿Quieres hacer una encuesta? Escribe ```.poll``` Y sigue los pasos''',
        brief='''Hace una encuesta''',
        description='''Hace una encuesta preguntandote por privado los campos que quieres que tenga''',
        usage='.poll'
    )
    async def poll(self, ctx):
        embed, emojis= await self.create_poll(ctx)
        try:
            await ctx.message.delete()
            msg = await ctx.send(embed=embed)
        except discord.Forbidden:
            msg = await ctx.author.dm_channel.send(embed=embed)

        for emoji in emojis:
            await msg.add_reaction(emoji)  