import discord
import asyncio
from discord.ext import commands
from classes.bot_class import context_is_admin

class tareas_commands(
    commands.Cog,
    name='Trabajos'
    ):
    '''Con estos comandos podrás ver y depende quién seas, editar, los trabajos y exmámenes
    que nos van mandando durante el curso. 
    Para mirar fechas de exámenes y trabajos, prueba *.trabajos ['''

    def __init__(self,bot):
        self.bot = bot
        Asignaturas={
            "Astronomía" : {

            },
            "Técnicas físicas II" : {

            },
            "Microondas: propagación y antenas": {

            },
            "Física cuántica I" : {

            },
            "Óptica" : {

            },
            "Termodinámica" : {

            },
            "Física de fluidos" : {

            },
            "Historia de la ciencia" : {

            },
            "Física de la atmósfera" : {

            },
            "Micro y nano sistemas" : {

            },
            "Física estadística" : {

            },
            "Física cuántica II" : {

            },
            "Láser y aplicaciones" : {

            },
            "Gravitación y cosmología" : {

            },
            "Caos y sistemas dinámicos no lineales" : {

            }
        }
    @commands.command(
        pass_context=True,
        aliases=['añadir'],
        help=''' asad''',
        brief='''añadir algo a la lista''',
        description='''asdasd''',
        usage='.....',
        [context_is_admin]
    )
    async def Añade(self, context, asignatura, titulo, *descripcion):
        for key in Asignaturas.key
            if key.find asignatura:
                name =asignatura
            else:
                await context.send('Parece que la asignatura que has puesto no existe')
        if name !=Null
        Asignaturas[name][titulo]=descripcion



    
)

