import discord

class FisTask():
    def __init__(self, task_id=None, subject='', title='', description='', day=None, month=None, year=None):
        self.id = task_id
        self.subject = subject
        self.title = title
        self.description = description
        self.day = day
        self.month = month
        self.year = year

        from ..database.tasks import ProyectsDB
        self.database = ProyectsDB()

    #def _create_db(self) -> Connection:...
    #def _connect(self) -> Connection:...
    #def add_task(self, task: FisTask) -> bool:...
    #def update_task(self, user: FisTask) -> bool:...
    #def del_task(self, user: FisTask) -> bool:...
    #def get_task(self, user_id) -> FisTask:...
    #def get_all_tasks(self) -> tuple:...
    #def get_all_subject_tasks(self, subject) -> tuple:...

    def embed(self) -> discord.Embed:
        '''Crea un mensaje tipo discord.Embed que muestra la tarea'''

        task_embed = discord.Embed(
            title='**{0.subject}**: *{0.title}*'.format(self),
            description='Fecha: {0.day}/{0.month}'.format(self) + ('/{0.year}'.format(self)) if self.year else '',
            color=discord.Color.purple()
        )

        if self.description:
            task_embed.add_field(
                name='**Descripcion:**',
                value=self.description if self.description else '*Sin especificar*',
                inline=False
            )

        task_embed.add_field(
                name='**Id={0.id}**'.format(self),
                value='Si cree necesaria alguna modificacion en este mensaje por favor pongase en contacto con algun moderador',
                inline=False
            )

        return task_embed