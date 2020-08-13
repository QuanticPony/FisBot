import discord
import asyncio
from discord.ext import commands
from classes.bot_class import context_is_admin


class Trabajo():
    def __init__(self, fecha, nombre, description):
        #*TODO: url a donde lo han mandado/foto
        self.fecha=fecha
        self.nombre=nombre
        self.description=description

    def Fecha(self):
        


class tareas_commands(
    commands.Cog,
    name='Trabajos'
    ):
    '''Con estos comandos podrás ver y depende quién seas, editar, los trabajos y exmámenes
    que nos van mandando durante el curso. 
    Para mirar fechas de exámenes y trabajos, prueba *.trabajos ['''

    def __init__(self, bot):
        self.bot = bot
        Asignaturas={
            "Astronomía" : [

            ],
            "Técnicas físicas II" : [

            ],
            "Microondas: propagación y antenas": [

            ],
            "Física cuántica I" : [

            ],
            "Óptica" : [

            ],
            "Termodinámica" : [

            ],
            "Física de fluidos" : [

            ],
            "Historia de la ciencia" : [

            ],
            "Física de la atmósfera" : [

            ],
            "Micro y nano sistemas" : [

            ],
            "Física estadística" : [

            ],
            "Física cuántica II" : [

            ],
            "Láser y aplicaciones" : [

            ],
            "Gravitación y cosmología" : [

            ],
            "Caos y sistemas dinámicos no lineales" : [

            ]
        }
    @commands.command(
        pass_context=True,
        aliases=['añadir'],
        help=''' asad''',
        brief='''añadir algo a la lista''',
        description='''asdasd''',
        usage='.....',
        check=[context_is_admin]
    )
    async def Añade(self, context, asignatura, titulo, *descripcion):
        for key in self.Asignaturas.key:
            name = ''
            if key.find(asignatura):
                name = key
            else:
                await context.send('Parece que la asignatura que has puesto no existe')
        if name:
            self.Asignaturas[name][titulo] = descripcion


    @commands.command(
        pass_context=True,
        aliases=['busca','mira','deberes'],
        help='''asdads''',
        brief='''asdasdasd''',
        description='''asdasdasd''',
        usage='sdasdasd'
    )

    async def comprobar(self, context, *asignaturas):
        lista_asignaturas=asignaturas.split(',')
        if len(lista_asignaturas)<1:
            await context.send("Bro que no has puesto ninguna")
        embed=discord.Embed(title="Trabajos pendientes", )
        for thing in lista_asignaturas:
            pass

