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
    Para mirar fechas de exámenes y trabajos, prueba ```.task list```'''

    def __init__(self, bot):
        self.bot = bot 
    
    # TODO  actualizar todo este cog

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
    async def task(self, context):
        pass
        

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

        task=FisTask(subject=subject, context=ctx)

        await task.create()
        return


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
                return await ctx.send('**Lo siento**. No hay trabajos ni examenes en la base de datos')

        else:
            if subject.isdigit():
                school_year = int(subject)
                if 0 < school_year < 5:
                    # TODO. Completar esto
                    tasks_list = FisTask().database.get_all_school_year_subjects()
                    pass
                else:
                    await ctx.send('Solo hay 4 cursos, y son enteros positivos distintos de 0') 
                return 


            subject = unicodedata.normalize('NFKD', subject)\
             .encode('ascii', 'ignore').decode('ascii').title()
            asignaturas = FisTask().database.subjects()

            for asignatura in asignaturas:
                if subject in asignatura:
                    subject = asignatura
                    break

            tasks_list = FisTask().database.get_all_subject_tasks(subject)
            embed = discord.Embed(
                title=subject + ' (Tareas/Examenes):',
                description='\t',
                color=discord.Color.purple()
            )

            if not tasks_list:
                return await ctx.send('''**Lo siento**. No hay trabajos ni examenes en la base de datos de la asignatura **{}**'''.format(subject))

        for task in tasks_list:
            description = f"id: {task.id} | " + f"Fecha: {task.day}/{task.month}" + f"/{task.year}" if task.year else '' 
            description += f" | [Fuente]({task.url})" if task.url else ''

            embed.add_field(
                name=f"{task.school_year}º -> **{task.subject}**: {task.title}",
                value=description,
                inline=False
            )
        
        return await ctx.send(ctx.author.mention,embed=embed) 


    @task.command(
        pass_context=True,
        aliases=['busca','mira'],
        help='''Quieres ver toda la informacion disponible de un cierto trabajo con id=14? ```.task get 14```
        Quieres mencionar a todo el mundo para enseñar la tarea de id=9 y decirles hola? ```.task get 9 @everyone Hola```''',
        brief='''Muestra la informacion relativa a un trabajo''',
        description='''Permite ver trabajos y examenes pendientes, asi como su fecha de entrega y una pequeña
            descripción de lo que hay que hacer, si hay algo que consideres que haya que cambiar de esta base 
            de datos, contacta con un moderador''',
        usage='.task get <task_id> [message]'
    )
    async def get(self, ctx, task_id, *args):
        task_id = unicodedata.normalize('NFKD', task_id)\
            .encode('ascii', 'ignore').decode('ascii')

        message_text = ' '.join(args)

        if task_id.isnumeric() and int(task_id) >= 0:
            task = FisTask().database.get_task(int(task_id))
            if task:
                await ctx.send(message_text, embed=task.embed())
            else:
                await ctx.send('No se ha encontrado nada en la base de datos con id={}'.format(task_id))
        else:
            await ctx.send('''**Lo siento**, pero la id de un elemento es un entero positivo. *{}* no es un entero positivo'''.format(task_id))

        if message_text:
            await ctx.message.delete()


    @task.command(
        pass_context=True,
        aliases=['del','quita','elimina'],
        help='''¿Quiere eliminar una tarea de id 14, por alguna razon magico-fantastica? ```.task delete 14```''',
        brief='''Elimina una tarea o examen de la base de datos''',
        description='''Permite eliminar un elemento de la tabla Tareas de la base de datos. Si lo que quiere es modificar una tarea, pruebe: ```.help task modify```''',
        usage='.task delete <task_id>',
        check=[context_is_admin]
    )
    async def delete(self, ctx, *, task_id):

        task_id = unicodedata.normalize('NFKD', task_id)\
            .encode('ascii', 'ignore').decode('ascii')

        if task_id.isnumeric() and int(task_id) >= 0:
            
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


    @task.command(
            pass_context=True,
            aliases=['asignaturas'],
            help='''¿Quieres ver la lista de asignaturas? ```.task subjects```''',
            brief='''Muestra las asignaturas de la base de datos''',
            description='''Muestra una lista de todas las asignaturas en la base de datos''',
            usage='.task subjects',
        )
    async def subjects(self, ctx):
        asignaturas = FisTask().database.subjects()

        embed = discord.Embed(
            title='Asignaturas en la base de datos:',
            description='''Si quieres informacion sobre las tareas de una asignatura en concreto prueba: 
                ```.task list [asignatura]```''',
            color=discord.Color.dark_purple()
        )
        asignaturas.sort()
        embed.add_field(
            name='Asignaturas actualmente activas:',
            value='-'+'\n-'.join(asignaturas),
            inline=False
            )
        embed.set_footer(text='Si falta alguna asignatura pongase en contacto con @mods')
        
        return await ctx.send(embed=embed)


    @task.command(
            pass_context=True,
            aliases=['modificar', 'mod'],
            help='''¿Quieres modificar la tarea de id 4? ```.task modify 4```''',
            brief='''Permite modificar una tarea o examen''',
            description='''Permite modificar una tarea o examen. Al llamar al comando aparece un mensaje
            embed que permite elegir los campos a cambiar''',
            usage='.task modify <task_id>',
            check=[context_is_admin]
        )
    async def modify(self, ctx, task_id):
        requested_task = FisTask().database.get_task(task_id)
        await requested_task.modify(ctx)
