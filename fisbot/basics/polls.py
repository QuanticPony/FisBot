import discord
import asyncio
import random
from discord.ext import commands
from ..classes.poll_class import Poll
from .. import context_is_admin
from ..classes.display_class import Display

class poll_cog(
    Display,
    commands.Cog, 
    name='Encuestas',
    ):
    '''Comandos para realizar encuestas. Pasos para realizar una: escriba ```.poll``` donde quiere que aparezca la encuesta.
    Cambia los campos de la encuesta por mensajes privados. Cuando este acabado pulsa 💾'''

    TIMEOUT = 300

    def __init__(self, bot):
        self.bot = bot


    async def create_poll(self, ctx) -> (discord.Embed, list):
        '''Crea una encuesta a traves de un dialogo por mensajes privados. Devuelve una `tupla` cuyos 
        elementos son el `embed` y una `lista` de las opciones respectivamente'''

        
        u = ctx.author
        c = u.dm_channel

        await ctx.message.delete()

        if not c:
            c = await u.create_dm()

        def confirm_reaction(reaction, user):
            return user.id == u.id
        def confirm_message(response_msg):
            return response_msg.author.id == u.id

        e = discord.Embed(
            title="📯 Título",
            description="🪕 Descripción",
            color=discord.Color.blurple()
            )
        e.add_field(
            name="Opciones",
            value="Reacciona con el emoticono que represente una nueva opcion",
            inline=False
        )

        poll_message = await c.send(embed=e)

        for i in ['📯', '🪕', '🎨', '🔺', '💾']:
            await poll_message.add_reaction(i)


        emoji= {}

        async def ask_field(embed) -> bool:
            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=self.TIMEOUT, check=confirm_reaction)
                emoj = str(reaction.emoji)

                if emoj == '💾':
                    return False, embed

                elif emoj == '🔺':
                    ask_message = await c.send('Quita la reaccion del campo que quieres eliminar')
                    reaction, user = await ctx.bot.wait_for('reaction_remove', timeout=self.TIMEOUT, check=confirm_reaction)
                    if str(reaction.emoji) in emoji.keys():
                        emoji.pop(str(reaction.emoji))
                    await ask_message.delete()

                elif emoj == '🎨':
                    ask_message = await c.send('Escribe el codigo RGB (0-255): (ej: 0 200 100)')
                    try:
                        response_msg = await ctx.bot.wait_for('message', timeout=self.TIMEOUT, check=confirm_message)
                        try:
                            r, g, b = map(int, response_msg.content.split())
                            title = embed.title
                            description = embed.description
                            new_e = discord.Embed(
                                title=title,
                                description=description,
                                color=discord.Color.from_rgb(r,g,b)
                            )
                            embed = new_e
                            await response_msg.add_reaction("✔️")
                        except :
                            await ask_message.delete()
                            await response_msg.add_reaction("❌")

                    except asyncio.TimeoutError:
                        await c.send('Se acabo el tiempo...')
                        return False, embed

                elif emoj =='📯':
                    try:
                        ask_message = await c.send('Escribe el nuevo titulo')
                        response_msg = await ctx.bot.wait_for('message', timeout=self.TIMEOUT, check=confirm_message)
                        try:
                            embed.title =  response_msg.content
                            await response_msg.add_reaction("✔️")
                        except:
                            await ask_message.delete()
                            await response_msg.add_reaction("❌")
                    except asyncio.TimeoutError:
                        await c.send('Se acabo el tiempo...')
                        return False, embed

                elif emoj =='🪕':
                    try:
                        ask_message = await c.send('Escribe la nueva descripccion')
                        response_msg = await ctx.bot.wait_for('message', timeout=self.TIMEOUT, check=confirm_message)
                        try:
                            embed.description =  response_msg.content
                            await response_msg.add_reaction("✔️")
                        except:
                            await ask_message.delete()
                            await response_msg.add_reaction("❌")
                    except asyncio.TimeoutError:
                        await c.send('Se acabo el tiempo...')
                        return False, embed
                    
                
                else:
                    ask_message = await c.send(f'Escribe la opcion que quieres añadir con el emoticono {emoj}')
                    try:
                        response_msg = await ctx.bot.wait_for('message', timeout=self.TIMEOUT, check=confirm_message)
                        try:
                            emoji.update({emoj : response_msg.content})
                            await response_msg.add_reaction("✔️")

                        except:
                            await ask_message.delete()
                            await response_msg.add_reaction("❌")

                    except asyncio.TimeoutError:
                        await c.send('Se acabo el tiempo...')
                        return False, embed
                return True, embed
            except:
                return False, embed

        check = True
        while check:
            check, e = await ask_field(e)
            e.clear_fields()
            frase = ''
            for emoj in emoji.keys():
                frase += f"{emoj} - {emoji[emoj]}\n"
            if not frase:
                frase = "Reacciona con el emoticono que represente una nueva opcion"
            e.add_field(
                name='Opciones:',
                value=frase,
                inline=False
                )
            await poll_message.edit(embed=e)

        try:
            want_user_confirm = await c.send("Quieres aparecer como creador de la encuesta? (Si:✅. No:❌)")
            await want_user_confirm.add_reaction("✅")
            await want_user_confirm.add_reaction("❌")

            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=30.0, check=confirm_reaction)
                if str(reaction.emoji) == "✅":
                    e.set_footer(text=u.nick, icon_url=str(u.avatar_url))

            except asyncio.TimeoutError:
                pass
        except asyncio.TimeoutError:
            pass
        return (e, emoji.keys())
        

    @commands.group(
        pass_context=True, 
        aliases=['encuesta','p'],
        help='''¿Quieres hacer una encuesta? Escribe ```.poll``` Y sigue los pasos
        ¿Quieres saber como funcionan las encuestas? ```.poll -tutorial```''',
        brief='''Hace una encuesta''',
        description='''Hace una encuesta preguntandote por privado los campos que quieres que tenga''',
        usage='.poll [-tutorial] [custom_message]'
    )
    async def poll(self, ctx, *, text=''):

        if text.startswith('-tutorial'):
            await self.tutorial(ctx)
            return

        embed, emojis= await self.create_poll(ctx)
        try:
            msg = await ctx.send(text, embed=embed)
            for emoji in emojis:
                await msg.add_reaction(emoji)
        except:
            pass
        
    async def tutorial(self, ctx):
        e = discord.Embed(
            title='Explicacion .poll',
            description='''Ten en cuenta que el bot no puede estar pendiente de ti todo el rato: 
            si te pide algo y no obtiene una respuesta en 5 minutos pasara a otra cosa''',
            color=discord.Color.from_rgb(38,236,227)
        )
        e.add_field(
            name='Como comenzar una encuesta?',
            value='''Escribe en el canal de texto donde quieras enviar la encuesta lo siguiente: 
            `.poll [Mensaje que quieres que acompañe a la encuesta]`. El mensaje entre [] es opcional.
            FisBot te enviara un mensaje por privado donde podras cambiar el titulo, descripcion, y opciones de la encuesta''',
            inline=False
            )
        e.add_field(
            name='Como cambiar el titulo o la descripcion de la encuesta?',
            value='''En el mensaje por privado de FisBot hay varias reacciones. Sirven para seleccionar el campo que quieres modificar.
            En cuanto lo selecciones FisBot te preguntara lo que quieres poner en ese campo. Y no seas impaciente, ve con calma que FisBot no es instantaneo''',
            inline=False
            )
        e.add_field(
            name='Como añadir una opcion?',
            value='''En las reacciones del mensaje de FisBot pulsa la reaccion 🔼. FisBot te preguntara por un emoticono y por la opcion.
            Hazle caso y todo saldra bien''',
            inline=False
            )
        e.add_field(
            name='Como eliminar una opcion?',
            value='''Pulsa la reaccion 🔺. FisBot te pedira que elimines la reaccion de la opcion a eliminar''',
            inline=False
            )
        e.add_field(
            name='Como cambiar el color?',
            value='''Pulsa la reaccion 🎨. FisBot te preguntara por el color en RGB de 0 a 255 (ej: 0 255 144). 
            Separadlos por espacios o comas, no por ambas. Y solo escribid eso''',
            inline=False
        )
        e.add_field(
            name='Como finalizo la encuesta?',
            value='''Esta accion es irreversible. Pulsa la reaccion 💾. FisBot te preguntara si quieres aparecer como creador de la encuesta.
            Reacciona acorde a lo que quieras y la encuesta se enviara''',
            inline=False
        )
        await ctx.send(f"{ctx.author.mention}",embed=e)
        
        