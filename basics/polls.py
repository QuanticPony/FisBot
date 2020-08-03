import discord
import asyncio
import random
from discord.ext import commands
from bot_class import context_is_admin

class poll(
    commands.Cog, 
    name='Encuestas',
    ):
    '''Comandos para realizar encuestas. Pasos para realizar una:
    \t1º: Poner un titulo a la encuesta: ```.polltitle <Titulo>```
    \t2º: Asegurarse de utilizar el separador adecuadamente, para ver cual hay: ```.separator```
    \t3º: En el caso de querer cambiar el separador: ```.separator <nuevo_separador>```
    \t4º: Dar los elementos de la encuesta separados por el separador actual (default:\'\_\'): ```.poll <elem1> _ <elem2> [ _ [...]]```'''

    def __init__(self, bot):
        self.bot = bot
        self.sep = '_'
        self.tit = 'Encuesta:'
    
    @commands.command(
        pass_context=True, 
        aliases=['encuesta','p'],
        help='''¿Grados o radianes, cual es mejor? Suponemos que el separador es el default: \_. Y que ya se ha introducido el titulo de la encuesta con *.polltitle*:
        ```.poll Grados_Radianes```''',
        brief='''Hace una encuesta''',
        description='''Hace una encuesta entre todos los elementos separados por el separador. Este se puede consultar con el comando **.separator**''',
        usage='.poll <elem1> separador <elem2> [separador [...]]'
    )
    async def poll(self, context, *, elementos):
        things_list = elementos.split(self.sep)
        if len(things_list) < 2:
            responses = [
                'Si señor, claro. Bien. Buena...',
                '\'Tamos tontos??',
                'Las encuestas suelen tener al menos 2 elementos',
                'Y las opciones? me las invento yo?',
                'lol no'
            ]
            things_list.append('NULL')
            await context.send(responses[random.randint(0,3)])
        if len(things_list) > 20:
            await context.send("Pero de que vas {0.message.author.mention}? Para que necesitas tantas opciones?".format(context))

        codepoint_start = 127462  # Letra A en unicode en emoji
        things_list = {chr(i): f"{chr(i)} - {v}" for i, v in enumerate(things_list, start=codepoint_start)}
        embed = discord.Embed(title=self.tit, description="\n".join(things_list.values()))
        await context.message.delete()
        message = await context.send( '@everyone',embed=embed)
        for reaction in things_list:
            await message.add_reaction(reaction) 
        self.tit = 'Encuesta:'


    @commands.command(
        pass_context=True, 
        aliases=['pollsep','sep','separador'],
        help='''¿Quiere hacer una encuesta y por casualidad en uno de los elementos a elegir hay una barra baja (\_)? 
        Puedes cambiar el separador a otro caracter diferente para poder poner lo que necesites. Pongamos que te interesa @ porque no te interfiere en nada:
        ```.separator @```''',
        brief='''Cambia el separador de .poll''',
        description='''Cambia la string de separacion de elementos de encuesta en el comando .poll''',
        usage='.separator [new_separator]'
    )
    async def separator(self, context, *separator):
        if separator:
            await context.message.delete()
            self.sep = separator[0]
        else:
            await context.send('Actualmente el separador de elementos de .poll es \'{0.sep}\''.format(self))


    @commands.command(
        pass_context=True, 
        aliases=['pollt','pt'],
        help='''¿Quiere hacer una encuesta para saber si son mejores los grados o los gradianes? ```.polltitle ¿Grados o radianes, cual es mejor?```''',
        brief='''Cambia el titulo de la encuesta .poll''',
        description='''Cambia el titulo de la encuesta .poll. Por defecto es \'Encuesta:\'''',
        usage='.polltitle [title...]'
    )
    async def polltitle(self, context, *,title):
        if title:
            await context.message.delete()
            self.tit = title
        else:
            await context.send('Actualmente el titulo de la encuesta de .poll es \'{0.tit}\''.format(self))
