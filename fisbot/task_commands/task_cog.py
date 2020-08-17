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
        description='''Añade un trabajo/examen a la base de datos de manera que haya fácil acceso para el resto de usuarios para luego mirar fechas de entrega''',
        usage='.Añade <nombre_asignatura> ... responder a las preguntas del bot',
    )
    async def _list(self, ctx, *, subject=None):
        if not subject:
            tasks_list = FisTask().database.get_all_tasks()
            embed = discord.Embed(
                title='Todas las tareas/examenes:',
                description='''Si quieres informacion sobre una asignatura en concreto prueba: 
                    ```.task list [asignatura]```''',
                color=discord.Color.purple()
            )
            if not tasks_list:
                await ctx.send('**Lo siento**. No hay trabajos ni examenes en la base de datos')

        else:
            subject = unicodedata.normalize('NFKD', subject)\
             .encode('ascii', 'ignore').decode('ascii').title()

            tasks_list = FisTask().database.get_all_subject_tasks(subject)
            embed = discord.Embed(
                title=subject + ' (Tareas/Examenes):',
                description='\t',
                color=discord.Color.purple()
            )

            if not tasks_list:
                await ctx.send('''**Lo siento**. No hay trabajos ni examenes en la base de datos de la asignatura **{}**'''.format(subject))

        for task in tasks_list:
            fecha = 'id: {0.id} | Fecha: {0.day}/{0.month}'.format(task)
            if task.year:
                fecha += '/{0.year}'.format(task)
            embed.add_field(
                name='**{0.subject}**: *{0.title}*'.format(task),
                value=fecha,
                inline=False
            )
        
        await ctx.send(ctx.author.mention,embed=embed)



    @task.command(
        pass_context=True,
        aliases=['busca','mira'],
        help='''Quieres ver toda la informacion disponible de un cierto trabajo con id=14? ```.task get 14```''',
        brief='''Muestra la informacion relativa a un trabajo''',
        description='''Permite ver trabajos y exámenes pendientes, así como su fecha de entrega y una pequeña
            descripción de lo que hay que hacer, si hay algo que consideres que haya que cambiar de esta base 
            de datos, contacta con un moderador''',
        usage='.task get <task_id>'
    )
    async def get(self, ctx, *, task_id): #comando para poder ver los trabajos que hay
        task_id = unicodedata.normalize('NFKD', task_id)\
            .encode('ascii', 'ignore').decode('ascii')

        if task_id.isnumeric() and int(task_id) >= 0: # Contiene una id
            task = FisTask().database.get_task(int(task_id))
            if task:
                await ctx.send('Esta es la tarea que pediste {.author.mention}:'.format(ctx), embed=task.embed())
            else:
                await ctx.send('No se ha encontrado nada en la base de datos con id={}'.format(task_id))
            return
        
        await ctx.send('''**Lo siento**, pero la id de un elemento es un entero positivo. *{}* no es un entero positivo'''.format(task_id))
        
        #lista_asignaturas=asignaturas.split(',')
        #if len(lista_asignaturas)<1:
        #    await context.send("Bro que no has puesto ninguna")
        #mensaje=''
        #for thing in lista_asignaturas:
        #    for key in self.Asignaturas:
        #        if thing in key:
        #            mensaje= mensaje+ *key* + '\n' #a falta de ponerlo en secciones, pone el nombre de cada asignatura en negrita
        #            for x in self.Asignatura[key]:
        #                mensaje= mensaje + x + '\n' #por cada elemento de la lista de cada asignatura añade un mensaje con su contenido, no se si habría que pasar por cada cosa de trabajo
        #embed=discord.Embed(title="Trabajos pendientes", description=mensaje)

    #@task.command(
    #    pass_context=True,
    #    aliases=['del','quita','elimina'],
    #    help='''vadvadv''',
    #    brief='''asbfafba''',
    #    description='''adfbafdbava''',
    #    usage='dvaisudnviansdv',
    #    check=[context_is_admin]
    #)
    #async def delete(self, context): #para quitar ctrabajos
    #     if ctx.message.author.id == original:
    #            original=ctx.message.author.id
    #            return True
    #        else: 
    #            return False
    #    original=context.message.author.id
    #    if not context.author.dm_channel:
    #        await context.author.create_dm()
    #    await context.author.dm_channel.send("Muy buenos días, de qué asignatura eliminas el trabajo?")
    #    asignatura = await client.wait_for('message', check=CompruebaAutor(ctx)) #No se como asegurar que le he pasado como parámetro a la función ctx, osea el contexto de quien lo manda
    #    i=0
    #    for key in self.Asignaturas:
    #        if asignatura in self.Asignaturas[i]:
    #            nombre_Asignatura=self.Asignaturas[i]
    #        i=i+1
    #    if nombre_Asignatura == Null:
    #        if not context.author.dm_channel:
    #        await context.author.create_dm()
    #    await context.author.dm_channel.send("No parece existir la asignatura de la que quieres borrar el nombre")
    #    else:
    #        mensaje = ''
    #        for x in self.Asignatura[nombre_Asignatura]:
    #            mensaje = mensaje + x + '\n'
    #        if not context.author.dm_channel:
    #        await context.author.create_dm()
    #    await context.author.dm_channel.send("Estos son los trabajos que hay, por favor introduce el número cardinal que corresponde al trabajo que quieras eliminar")
    #    eliminar = await client.wait_for('message', check=CompruebaAutor(ctx))
    #    eliminar = eliminar - 1 #como es una lista, si quieres eliminar el trabajo 1 será el elemento 0
    #    self.Asignatura[nombre_Asignatura].pop(eliminar)
    #    if not context.author.dm_channel:
    #        await context.author.create_dm()
    #    await context.author.dm_channel.send("Muchas gracias, ten un buen día")