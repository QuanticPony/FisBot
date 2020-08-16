import discord
import asyncio
import unicodedata
from discord.ext import commands
from ..classes.bot_class import context_is_admin
from ..classes.task_class import FisTask
        


class task_commands(
    commands.Cog,
    name='Trabajos y Examenes'
    ):
    '''Con estos comandos podrás ver y depende quién seas, editar, los trabajos y exmámenes
    que nos van mandando durante el curso. 
    Para mirar fechas de exámenes y trabajos, prueba *.trabajos ['''

    def __init__(self, bot):
        self.bot = bot #defino un diccionario que hará de base de datos de los trabajos
    

    @commands.group(
        pass_context=True,
        aliases=['añadir'],
        help='''Quiero añadir un trabajo de astro? .Añade Astro, y luego tocará una conversa
        ción agradable con el bot en la que introduzco fecha, nombre y descripcion''',
        brief='''Añade un trabajo/examen''',
        description='''Añade un trabajo/examen a la base de datos de manera que haya fácil acceso
        para el resto de usuarios para luego mirar fechas de entrega''',
        usage='.Añade <nombre_asignatura> ... responder a las preguntas del bot',
        check=[context_is_admin]
    )
    async def task(self, context):...
        

    @task.command(
        pass_context=True,
        aliases=['añadir'],
        help='''Quiero añadir un trabajo de astro? ```.task add Astro``` 
        y luego tocará una conversación agradable con el bot en la que introduzco fecha, nombre y descripcion''',
        brief='''Añade un trabajo/examen''',
        description='''Añade un trabajo/examen a la base de datos de manera que haya fácil acceso
        para el resto de usuarios para luego mirar fechas de entrega''',
        usage='.Añade <nombre_asignatura> ... responder a las preguntas del bot',
        check=[context_is_admin]
    )
    async def add(self, ctx, subject):
        task=FisTask(subject=subject)
        msg_out = await ctx.send('Escribe el titulo del trabajo/examen:')
        def confirm(msg_in):
            return ctx.message.author.id == msg_in.author.id
        try:
            msg_in = await self.bot.wait_for('message', timeout=30.0, check=confirm)
        except asyncio.TimeoutError:
            await msg_out.delete()
        
        # TODO: que este normalizado
        task.title = unicodedata.normalize('NFKD', msg_in.content)\
            .encode('ascii', 'ignore').decode('ascii').title()

        msg_out = await ctx.send('Escribe la descripcion:')
        try:
            msg_in = await self.bot.wait_for('message', timeout=30.0, check=confirm)
        except asyncio.TimeoutError:
            await msg_out.delete()
        task.description = unicodedata.normalize('NFKD', msg_in.content)\
            .encode('ascii', 'ignore').decode('ascii').title()

        msg_out = await ctx.send('Escribe la fecha limite/entrega/examen: ```<day/month>[/year]```')
        try:
            msg_in = await self.bot.wait_for('message', timeout=30.0, check=confirm)
        except asyncio.TimeoutError:
            await msg_out.delete()
        date = msg_in.content.split('/')
        print(date)
        self.day = int(date[0])
        self.month = date[1]
        try:
            self.year = int(date[2])  
        except:
            self.year = 2020

        task.database.add_task(task)


        
    @task.command(
        pass_context=True,
        name='list',
        aliases=['lista'],
        help='''Quiero añadir un trabajo de astro? ```.task add Astro``` 
        y luego tocará una conversación agradable con el bot en la que introduzco fecha, nombre y descripcion''',
        brief='''Añade un trabajo/examen''',
        description='''Añade un trabajo/examen a la base de datos de manera que haya fácil acceso
        para el resto de usuarios para luego mirar fechas de entrega''',
        usage='.Añade <nombre_asignatura> ... responder a las preguntas del bot',
    )
    async def _list(self, ctx, *, subject=None):
        if not subject:
            tasks_list = FisTask().database.get_all_tasks()
            embed = discord.Embed(
                title='Todas las tareas/examenes:',
                description='\t',
                color=discord.Color.magenta()
            )
        else:
            subject = unicodedata.normalize('NFKD', subject)\
             .encode('ascii', 'ignore').decode('ascii').title()

            tasks_list = FisTask().database.get_all_subject_tasks(subject)
            embed = discord.Embed(
                title=subject + ' (Tareas/Examenes):',
                description='\t',
                color=discord.Color.magenta()
            )

        if len(tasks_list)==0:
            await ctx.send('No hay trabajos ni examenes en la base de datos de la asignatura **{}**'.format(subject))

        for task in tasks_list:
            fecha = 'Fecha: {0.day}/{0.month}'.format(task)
            if task.year:
                fecha += '/{0.year}'.format(task)
            embed.add_field(
                name=task.title,
                value=fecha,
                inline=False
            )
        
        await ctx.send(ctx.author.mention,embed=embed)

        
#
#
#    @commands.command( #lo tipico de los comandos
#        pass_context=True,
#        aliases=['añadir'],
#        help='''Quiero añadir un trabajo de astro? .Añade Astro, y luego tocará una conversa
#        ción agradable con el bot en la que introduzco fecha, nombre y descripcion''',
#        brief='''Añade un trabajo/examen''',
#        description='''Añade un trabajo/examen a la base de datos de manera que haya fácil acceso
#        para el resto de usuarios para luego mirar fechas de entrega''',
#        usage='.Añade <nombre_asignatura> ... responder a las preguntas del bot',
#        check=[context_is_admin]
#    )
#    async def añade(self, context): #funcion para añadir un trabajo nuevo, si eres admin
#        def _CompruebaAutor(ctx, original): #funcion que en principio comprueba si la id que le han pasado como parametro es la misma que una id original
#            if ctx.message.author.id == original:
#                original=ctx.message.author.id
#                return True
#            else: 
#                return False
#        # Lo que has hecho esta mas o menos bien, salvo porque original tiene que ser un imput de la funcion. Pero es mas correcto de la siguiente manera:
#        def CompruebaAutor(context):
#            return ctx.message.author.id == original_ctx.author.id
#
#        original_ctx=context
#        if not context.author.dm_channel: #el if este que hay que ponerlo para mandar un dm
#            await context.author.create_dm()
#    
#        await context.author.dm_channel.send("Muy buenos dias, a que asignatura añades el trabajo?")
#        try:
#            msg = await client.wait_for('message', timeout== 30.0, check=CompruebaAutor)
#        except asyncio.TimeoutError:
#            return
#
#
#        asignatura = unicodedata.normalize('NFKD', msg.content)\
#            .encode('ascii', 'ignore').decode('ascii').title()
#
#
#        for i in range(0,1):
#            try:
#                pass
#                # TODO: Ver si asignatura esta en la base de datos
#            except:
#                pass
#                # preguntar de nuevo
#        else:
#            await context.author.dm_channel.send('Anda, vuelve a escribir el comando si quieres hacer algo')
#            return
#
#        # En lo siguiente has puesto muchas veces lo de crear un canal dm. No es necesario porque ya lo has creado arriba
#         
#        #cuando tenemos el nombre de la asignatura bien recolectamos los datos necesarios para definir un trabajo nuevo
#
#        #TODO crear categoría especial para examen
#
#        await context.author.dm_channel.send("Ahora dime la fecha de entrega del trabajo/fecha de examen") 
#
#        msg = await client.wait_for('message',check=CompruebaAutor(ctx))
#       
#        await context.author.dm_channel.send("Bien, queda poco, a continuación ponle un nombre al trabajo/examen")
#        nombre = await client.wait_for('message', check=CompruebaAutor(ctx))
#        
#        await context.author.dm_channel.send("Por último, añade una descripción al trabajo/examen")
#        descripcion = await client.wait_for('message',check=CompruebaAutor(ctx))
#        Trabajo1= Trabajo(fecha,nombre,descripcion) 
#        self.Asignaturas[nombre_Asignatura].append(Trabajo1) #añadimos al final de la lista un nuevo trabajo
#
#
#
#
#
#
#
#    @commands.command(
#        pass_context=True,
#        aliases=['busca','mira','deberes'],
#        help='''Quieres ver que trabajos hay de fluidos? .comprobar fluidos''',
#        brief='''Permite ver trabajos pendientes''',
#        description='''Permite ver trabajos y exámenes pendientes, así como su fecha de entrega y una pequeña descripción
#        de lo que hay que hacer, si hay algo que consideres que haya que cambiar de esta base de datos, contacta con un moderador''',
#        usage='.comprobar <asigatura> [, <asignatura2>,...]'
#    )
#    async def comprobar(self, context, *asignaturas): #comando para poder ver los trabajos que hay
#        lista_asignaturas=asignaturas.split(',')
#        if len(lista_asignaturas)<1:
#            await context.send("Bro que no has puesto ninguna")
#        mensaje=''
#        for thing in lista_asignaturas:
#            for key in self.Asignaturas:
#                if thing in key:
#                    mensaje= mensaje+ *key* + '\n' #a falta de ponerlo en secciones, pone el nombre de cada asignatura en negrita
#                    for x in self.Asignatura[key]:
#                        mensaje= mensaje + x + '\n' #por cada elemento de la lista de cada asignatura añade un mensaje con su contenido, no se si habría que pasar por cada cosa de trabajo
#        embed=discord.Embed(title="Trabajos pendientes", description=mensaje)
#
#
#
#
#
#
#
#
#    @commands.comand(
#        pass_context=True,
#        aliases=['quita','elimina'],
#        help='''vadvadv''',
#        brief='''asbfafba''',
#        description='''adfbafdbava''',
#        usage='dvaisudnviansdv',
#        check=[context_is_admin]
#    )
#    async def quitar(self, context): #para quitar ctrabajos
#         if ctx.message.author.id == original:
#                original=ctx.message.author.id
#                return True
#            else: 
#                return False
#        original=context.message.author.id
#        if not context.author.dm_channel:
#            await context.author.create_dm()
#        await context.author.dm_channel.send("Muy buenos días, de qué asignatura eliminas el trabajo?")
#        asignatura = await client.wait_for('message', check=CompruebaAutor(ctx)) #No se como asegurar que le he pasado como parámetro a la función ctx, osea el contexto de quien lo manda
#        i=0
#        for key in self.Asignaturas:
#            if asignatura in self.Asignaturas[i]:
#                nombre_Asignatura=self.Asignaturas[i]
#            i=i+1
#        if nombre_Asignatura == Null:
#            if not context.author.dm_channel:
#            await context.author.create_dm()
#        await context.author.dm_channel.send("No parece existir la asignatura de la que quieres borrar el nombre")
#        else:
#            mensaje = ''
#            for x in self.Asignatura[nombre_Asignatura]:
#                mensaje = mensaje + x + '\n'
#            if not context.author.dm_channel:
#            await context.author.create_dm()
#        await context.author.dm_channel.send("Estos son los trabajos que hay, por favor introduce el número cardinal que corresponde al trabajo que quieras eliminar")
#        eliminar = await client.wait_for('message', check=CompruebaAutor(ctx))
#        eliminar = eliminar - 1 #como es una lista, si quieres eliminar el trabajo 1 será el elemento 0
#        self.Asignatura[nombre_Asignatura].pop(eliminar)
#        if not context.author.dm_channel:
#            await context.author.create_dm()
#        await context.author.dm_channel.send("Muchas gracias, ten un buen día")