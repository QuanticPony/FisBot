import discord
import asyncio
import unicodedata
from discord.ext import commands
from classes.bot_class import context_is_admin


class Trabajo(): #definimos clase trabajo para poder meterle fechas, descripciones...
    def __init__(self, fecha, nombre, description):
        #*TODO: url a donde lo han mandado/foto
        if fecha:
            self.fecha = fecha
        if nombre:
            self.nombre=nombre
        if description:
            self.description=description
     #definimos las funciones que podamos usar para cada cosa
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
        self.bot = bot #defino un diccionario que hará de base de datos de los trabajos
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
    @commands.command( #lo tipico de los comandos
        pass_context=True,
        aliases=['añadir'],
        help='''Quiero añadir un trabajo de astro? .Añade Astro, y luego tocará una conversa
        ción agradable con el bot en la que introduzco fecha, nombre y descripción''',
        brief='''Añade un trabajo/examen''',
        description='''Añade un trabajo/examen a la base de datos de manera que haya fácil acceso
        para el resto de usuarios para luego mirar fechas de entrega''',
        usage='.Añade <nombre_asignatura> ... responder a las preguntas del bot',
        check=[context_is_admin]
    )
    async def Añade(self, context): #funcion para añadir un trabajo nuevo, si eres admin
        def CompruebaAutor(ctx,original): #funcion que en principio comprueba si la id que le han pasado como parametro es la misma que una id original
            if ctx.message.author.id == original:
                original=ctx.message.author.id
                return True
            else: 
                return False
        # Lo que has hecho esta mas o menos bien, salvo porque original tiene que ser un imput de la funcion. Pero es mas correcto de la siguiente manera:
        def _CompruebaAutor(ctx, original):
            return ctx.message.author.id == original

        

        original=context.message.author.id
        if not context.author.dm_channel: #el if este que hay que ponerlo para mandar un dm
            await context.author.create_dm()
        await context.author.dm_channel.send("Muy buenos días, a qué asignatura añades el trabajo?")
        try:
            msg = await client.wait_for('message', timeout== 60.0, check=CompruebaAutor(ctx)) # No se como asegurar que le he pasado como parámetro a la función ctx, osea el contexto de quien lo manda
                                                                                     # Solo hace falta cambiar el parametro de CompruebaAutor a context, y no ctx
        except asyncio.TimeoutError:
            return


        asignatura = unicodedata.normalize('NFKD', msg.content)\
            .encode('ascii', 'ignore').decode('ascii').title()

        
        while not
        try:
            # TODO: Ver si asignatura esta en la base de datos
        except:
            


        for key in self.Asignaturas.keys():
            if asignatura in key:
                nombre_Asignatura = key #es un intento de que el nombre de la asignautra se reemplace por el nombre completo de la key del diccoinario
                                        #porque me preocupa que si por ejemplo nombre asignatura es Termo, en vez de meterlo en Termodinamica 
                                        #cree una nueva key llamado termo y lo meta ahi, asi si Termo esta en termodinamica, el nombre de la asignatura 
                                        #sera termodinamica, no estoy seguro que lo pueda hacer asi con la i tan facil pero es la idea
                break # Esto es para que salga del bucle for. Y asi key ya sera el nombre de la asignatura
        else:
            await context.author.dm_channel.send('No existe tal asignatura, pruebe de nuevo: (compruebe que este bien escrita)')
            return context.command.

        
        if nombre_Asignatura == Null:
            if not context.author.dm_channel:
                await context.author.create_dm()
            await context.author.dm_channel.send('No existe tal asignatura, repite el proceso')#TODO que sea un bucle

        # En lo siguiente has puesto muchas veces lo de crear un canal dm. No es necesario porque ya lo has creado arriba
        else: 
        #cuando tenemos el nombre de la asignatura bien recolectamos los datos necesarios para definir un trabajo nuevo

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
            self.Asignaturas[nombre_Asignatura].append(Trabajo1) #añadimos al final de la lista un nuevo trabajo

    @commands.command(
        pass_context=True,
        aliases=['busca','mira','deberes'],
        help='''Quieres ver que trabajos hay de fluidos? .comprobar fluidos''',
        brief='''Permite ver trabajos pendientes''',
        description='''Permite ver trabajos y exámenes pendientes, así como su fecha de entrega y una pequeña descripción
        de lo que hay que hacer, si hay algo que consideres que haya que cambiar de esta base de datos, contacta con un moderador''',
        usage='.comprobar <asigatura> [, <asignatura2>,...]'
    )

    async def comprobar(self, context, *asignaturas): #comando para poder ver los trabajos que hay
        lista_asignaturas=asignaturas.split(',')
        if len(lista_asignaturas)<1:
            await context.send("Bro que no has puesto ninguna")
        mensaje=''
        for thing in lista_asignaturas:
            for key in self.Asignaturas:
                if thing in key:
                    mensaje= mensaje+ *key* + '\n' #a falta de ponerlo en secciones, pone el nombre de cada asignatura en negrita
                    for x in self.Asignatura[key]:
                        mensaje= mensaje + x + '\n' #por cada elemento de la lista de cada asignatura añade un mensaje con su contenido, no se si habría que pasar por cada cosa de trabajo
        embed=discord.Embed(title="Trabajos pendientes", description=mensaje)

    @commands.comand(
        pass_context=True,
        aliases=['quita','elimina'],
        help='''vadvadv'''
        brief='''asbfafba'''
        description='''adfbafdbava'''
        usage='dvaisudnviansdv',
        check=[context_is_admin]
    )

    async def quitar(self, context): #para quitar ctrabajos
         if ctx.message.author.id == original:
                original=ctx.message.author.id
                return True
            else: 
                return False
        original=context.message.author.id
        if not context.author.dm_channel:
            await context.author.create_dm()
        await context.author.dm_channel.send("Muy buenos días, de qué asignatura eliminas el trabajo?")
        asignatura = await client.wait_for('message', check=CompruebaAutor(ctx)) #No se como asegurar que le he pasado como parámetro a la función ctx, osea el contexto de quien lo manda
        i=0
        for key in self.Asignaturas:
            if asignatura in self.Asignaturas[i]:
                nombre_Asignatura=self.Asignaturas[i]
            i=i+1
        if nombre_Asignatura == Null:
            if not context.author.dm_channel:
            await context.author.create_dm()
        await context.author.dm_channel.send("No parece existir la asignatura de la que quieres borrar el nombre")
        else:
            mensaje = ''
            for x in self.Asignatura[nombre_Asignatura]:
                mensaje = mensaje + x + '\n'
            if not context.author.dm_channel:
            await context.author.create_dm()
        await context.author.dm_channel.send("Estos son los trabajos que hay, por favor introduce el número cardinal que corresponde al trabajo que quieras eliminar")
        eliminar = await client.wait_for('message', check=CompruebaAutor(ctx))
        eliminar = eliminar - 1 #como es una lista, si quieres eliminar el trabajo 1 será el elemento 0
        self.Asignatura[nombre_Asignatura].pop(eliminar)
        if not context.author.dm_channel:
            await context.author.create_dm()
        await context.author.dm_channel.send("Muchas gracias, ten un buen día")