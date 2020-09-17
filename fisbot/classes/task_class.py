import discord
import asyncio
from .display_class import Display

class FisTask(Display):

    _title_for_new = 'Crear tarea'
    _title_for_mod = 'Modificar **{0.subject}**: *{0.title}*'
    _title_for_del = 'Eliminar **{0.subject}**: *{0.title}* id= {0.id}'

    _descr_for_new ='''Abajo tienes la lista de todos los campos modificables. 
        Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
        *Cuando hayas acabado* presiona el boton de guardar'''
    _descr_for_mod ='''Abajo tienes la lista de todos los campos modificables. 
        Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
        *Cuando hayas acabado* presiona el boton de guardar'''
    _descr_for_del ='''¿Seguro que quiere eliminar este elemento de la base de datos?
        Si es así, reaccione ✅. De lo contrario, reaccione ❌:'''

    def __init__(self, task_id=None, subject='', title='', description='', day=0, month=0, year=0, school_year = 0, url='', context=None):
        super().__init__(context=context)
        self.id = task_id
        self.subject = subject
        self.title = title
        self.description = description
        self.day = day
        self.month = month
        self.year = year
        self.school_year = school_year
        self.url = url

        from ..database.tasks import ProyectsDB
        self.database = ProyectsDB

        if context:
            self._ctx = context




# Funciones sobreescritas de la clase Display

    def embed_show(self) -> discord.Embed:
        '''Devuelve un mensaje tipo `discord.Embed` que muestra la tarea'''

        task_embed = discord.Embed(
            title=f"**{self.school_year}º -> {self.subject}**",
            description=f"**{self.title}**" + (f"[URL]({self.url})" if self.url else ''),
            color=discord.Color.purple()
        )
        task_embed.add_field(
            name='Fecha:',
            value='{0.day}/{0.month}'.format(self) + ('/{0.year}'.format(self)) if self.year else '',
            inline=True
        )
        task_embed.add_field(
            name='Id:',
            value=f'**{self.id}**',
            inline=True
        )
        task_embed.add_field(
            name='**Descripcion:**',
            value=self.description if self.description else '*Sin especificar*',
            inline=False
        )
        task_embed.set_footer(text='Si cree necesaria alguna modificacion en este mensaje por favor pongase en contacto con algun moderador (@mods)')

        return task_embed

    async def discord_obj(self):
        return await super().discord_obj()

    async def update_discord_obj(self):
        return await super().update_discord_obj()

    async def save_in_database(self) -> bool:
        '''Guarda la tarea en la base de datos'''

        self.database.add_task(self)
        return self.database.update_task(self)

    async def remove_from_database(self) -> bool:
        '''Borra la tarea de la base de datos'''

        return self.database.del_task(self)



    def title_for_new(self) -> str:

        return self._title_for_new.format(self)

    def title_for_mod(self) -> str:

        return self._title_for_mod.format(self)

    def title_for_del(self) -> str:
        return self._title_for_del.format(self)


    def description_for_new(self) -> str:

        return self._descr_for_new.format(self)

    def description_for_mod(self) -> str:

        return self._descr_for_mod.format(self)

    def description_for_del(self) -> str:

        return  self._descr_for_del.format(self)

    def prepare_atributes_dic(self):
        '''Prepara los diccionarios internos para trabajar con ellos'''

        self._atributes_dic = self.__dict__.copy()

        for key in ['id', 'database']:
            try:
                self._atributes_dic.pop(key)
            except KeyError:
                continue

        