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
        self.bot = bot 
    

    @commands.group(
        pass_context=True,
        aliases=['añadir'],
        help='''¿Quiere ver una lita de todas las tareas?```.task list```
        ¿Quieres ver una lista de tareas de la asignatura Informatica?```.task list inFórmAtiCa```
        ¿Eres moderador y quieres añadir una tarea a la asignatura Informatica?```.task add INfóRmaticÁ```
        ¿Eres moderador y quieres cambiar una tarea con id 14?```.task modify 14```
        ¿Eres moderador y quieres borrar una tarea con id 1205?```.task delete 1205```''',
        brief='''Conjunto de comandos para administrar las tareas''',
        description='''Engloba el conjunto de comandos para modificar, añadir, y borrar tareas y examenes de la base de datos''',
        usage='.task <order> [args]'
    )
    async def task(self, context):... #what is this
        
        

    @task.command(
        pass_context=True,
        aliases=['añadir'],
        help='''Quiero añadir un trabajo de astro? ```.task add Astro``` 
        y luego tocará una conversación agradable con el bot en la que introduzco fecha, nombre y descripcion''',
        brief='''Añade un trabajo/examen''',
        description='''Añade un trabajo/examen a la base de datos de manera que haya fácil acceso
        para el resto de usuarios para luego mirar fechas de entrega''',
        usage='.task add <nombre_asignatura> <+ responder a las preguntas del bot>',
        check=[context_is_admin]
    )
    async def add(self, ctx, subject):
        task=FisTask(subject=subject) #esto es la base de datos?
        msg_out = await ctx.send('Escribe el titulo del trabajo/examen:') #entonces no hay dms?
        def confirm(msg_in):
            return ctx.message.author.id == msg_in.author.id #ah, asi se puede definir
        try:
            msg_in = await self.bot.wait_for('message', timeout=30.0, check=confirm) #esto es para que si no responde nunca pare no?
        except asyncio.TimeoutError:
            await msg_out.delete()
        

        task.title = unicodedata.normalize('NFKD', msg_in.content)\
            .encode('ascii', 'ignore').decode('ascii').title() #NFKD? y ahora estas pasando el titulo a ascii?

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
        self.day = int(date[0])
        self.month = date[1]
        try:
            self.year = int(date[2])  #esto pilla la fecha del ordenador asumo, y el 2?
        except:
            self.year = 2020 

        task.database.add_task(task)


        
    @task.command(
        pass_context=True,
        name='list',
        aliases=['lista'],
        help='''¿Quieres ver la lista de todos los trabajos y examenes? ```.task list```
        ¿Quieres ver todos los examenes y tareas de la asignatura de electromagnetismo pero no sabes escribir bien? ```.task list eLeCtrOMágnetisMo```''',
        brief='''Muestra una lista de trabajos y examenes''',
        description='''Permite ver la lita completa de tareas y examenes de la base de datos. Tanto de todas las asignaturas, como de alguna en concreto''',
        usage='.task list [subject]',
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

    #Entonces, el comando que acaba de acabar en la 132 le pones una asignatura y te dice todos los trabajos, y el de abajo le dices una id y te da toda la descripcion no?

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
        
        #if ctx.message.author.id == original:
        #        original=ctx.message.author.id
        #        return True
        #    else: 
        #        return False
        #original=context.message.author.id
        #if not context.author.dm_channel:
        #    await context.author.create_dm()
        #await context.author.dm_channel.send("Muy buenos días, de qué asignatura eliminas el trabajo?")
        #asignatura = await client.wait_for('message', check=CompruebaAutor(ctx)) #No se como asegurar que le he pasado como parámetro a la función ctx, osea el contexto de quien lo manda
        #i=0
        #for key in self.Asignaturas:
        #    if asignatura in self.Asignaturas[i]:
        #        nombre_Asignatura=self.Asignaturas[i]
        #    i=i+1
        #if nombre_Asignatura == Null:
        #    if not context.author.dm_channel:
        #    await context.author.create_dm()
        #await context.author.dm_channel.send("No parece existir la asignatura de la que quieres borrar el nombre")
        #else:
        #    mensaje = ''
        #    for x in self.Asignatura[nombre_Asignatura]:
        #        mensaje = mensaje + x + '\n'
        #    if not context.author.dm_channel:
        #    await context.author.create_dm()
        #await context.author.dm_channel.send("Estos son los trabajos que hay, por favor introduce el número cardinal que corresponde al trabajo que quieras eliminar")
        #eliminar = await client.wait_for('message', check=CompruebaAutor(ctx))
        #eliminar = eliminar - 1 #como es una lista, si quieres eliminar el trabajo 1 será el elemento 0
        #self.Asignatura[nombre_Asignatura].pop(eliminar)
        #if not context.author.dm_channel:
        #    await context.author.create_dm()
        #await context.author.dm_channel.send("Muchas gracias, ten un buen día")
       

    @task.command(
        pass_context=True,
        aliases=['del','quita','elimina'],
        help='''¿Quiere eliminar una tarea de id 14, por alguna razon magico-fantastica? ```.task delete 14```''',
        brief='''Elimina una tarea o examen de la base de datos''',
        description='''Permite eliminar un elemento de la tabla Tareas de la base de datos. Si lo que quiere es modificar una tarea, pruebe: ```.help task modify```''',
        usage='.task delete <task_id>',
        check=[context_is_admin]
    )
    async def delete(self, ctx, *, task_id): #para quitar trabajos

        task_id = unicodedata.normalize('NFKD', task_id)\
            .encode('ascii', 'ignore').decode('ascii')

        if task_id.isnumeric() and int(task_id) >= 0: # Contiene una id
            
            task = FisTask().database.get_task(int(task_id))

            if task:

                msg_conf = await ctx.send('¿Seguro que quiere borrar esto de la base de datos {.author.mention}?'.format(ctx),embed=task.embed())
                await msg_conf.add_reaction("✅")
                await msg_conf.add_reaction("❌")

                def confirm(reaction, user):
                    return str(reaction.emoji) == '✅' and ctx.message.author == user

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=10.0, check=confirm)
                except asyncio.TimeoutError:
                    await msg_conf.delete()
                else:
                    task.database.del_task(task)
                    await ctx.message.delete()
                    await msg_conf.delete()
                return


            else:
                await ctx.send('No se ha encontrado nada en la base de datos con id={}'.format(task_id))
            return


        await ctx.send('''**Lo siento**, pero la id de un elemento es un entero positivo. *{}* no es un entero positivo'''.format(task_id))


import datetime

async def reminders():
    loop = asyncio.get_running_loop() #nos dará el loop del evento que este ejecutandose en el momenot, con su tiempo de ejecución
    end_time = loop.time() #el tiempo de acabar será ahora, para que solo lo haga una vez
    today = date.today()
    while True:
        tasks_list = FisTask().database.get_all_subject_tasks(subject)
        for task in tasks_list:
            month_task = '{0.month}'.format(task)
            day_task = '{0.day}'.format(task) #no se si esto y lo anterior se tiene que poner así o hay modo simplificado, pero de momento lo dejo asi
            month = today.strftime("%m") #en los ejemplos que he visto de sacar la fecha de hoy siempre saca los tres de golpe, con lo que no se si solo funciona si sacas los tres en una string y leugo los separo, dejo comentado un código que haría eso
            day = today.strftime("%d")
            #today = today.strftime("%d/%m/%Y")
            #date = today.split("/")
            if month_task == month: #en caso de usar la string poner date[1], no he comparado años de momento pues no se por que la verdad, si esto va añadiré los años
                if day_task - day == 2:  #en caso de usasr la string poner date[0] he intentado poner un || con mas casos pero no le ha gustado no se por que
                    await ctx.send('Quedan 2 días para la entrega de la tarea con id= {}'.format(task))
        if loop.time()+1.0 >= end_time:
            break
        await asyncio.sleep(24*60*60) #ahora debería dormir 24 horas

asyncio.run(reminders())
        