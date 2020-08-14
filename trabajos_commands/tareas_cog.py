import discord
import asyncio
from discord.ext import commands
from classes.bot_class import context_is_admin


class Trabajo():
    def __init__(self, fecha, nombre, description):
        #*TODO: url a donde lo han mandado/foto
        if fecha:
            self.fecha = fecha
        if nombre:
            self.nombre=nombre
        if description:
            self.description=description

    def add_date(self, fecha):
        self.fecha = fecha
    def add_description(self, description):
        self.description= description
        


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
    async def Añade(self, context):
        def CompruebaAutor(ctx):
            if ctx.message.author.id == original:
                original=ctx.message.author.id
                return True
            else: 
                return False
        original=context.message.author.id
        if not context.author.dm_channel:
            await context.author.create_dm()
        await context.author.dm_channel.send("Muy buenos días, a qué asignatura añades el trabajo?")
        asignatura = await client.wait_for('message', check=CompruebaAutor(ctx)) #No se como asegurar que le he pasado como parámetro a la función ctx, osea el contexto de quien lo manda
        i=0
        for key in self.Asignaturas:
            if asignatura in self.Asignaturas[i]
                nombre_Asignatura=self.Asignaturas[i]#es un intento de que el nombre de la asignautra se reemplace por el nombre completo de la key del diccoinario
                                                    #porque me preocupa que si por ejemplo nombre asignatura es Termo, en vez de meterlo en Termodinamica 
                                                    #cree una nueva key llamado termo y lo meta ahi, asi si Termo esta en termodinamica, el nombre de la asignatura 
                                                    #sera termodinamica, no estoy seguro que lo pueda hacer asi con la i tan facil pero es la idea
        i=i+1
        else: 
            if not context.author.dm_channel:
                await context.author.create_dm()
            await context.author.dm_channel.send('No existe tal asignatura, repite el proceso')#TODO que sea un bucle
        if nombre_Asignatura!=Null:
            if not context.author.dm_channel:
                await context.author.create_dm()
            await context.author.dm_channel.send("Ahora dime la fecha de entrega del trabajo/fecha de examen")#TODO crear categoría especial para examen
            fecha = await client.wait_for('message',check=CompruebaAutor(ctx))
            if not context.author.create_dm()
                await context.author.create_dm()
            await context.author.dm_channel.send("Bien, queda poco, a continuación ponle un nombre al trabajo/examen")
            nombre = await client.wait_for('message', check=CompruebaAutor(ctx))
            if not context.author.create_dm()
                await context.author.create_dm()
            await context.author.dm_channel.send("Por último, añade una descripción al trabajo/examen")
            descripcion = await client.wait_for('message',check=CompruebaAutor(ctx))
            Trabajo1= Trabajo(fecha,nombre,descripcion)
            self.Asignaturas[nombre_Asignatura]=Trabajo1




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

