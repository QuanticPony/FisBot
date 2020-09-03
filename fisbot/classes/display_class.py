import discord
import asyncio
from discord.ext import commands

class Display():

    CODEPOINT_START = 127462  # Letra A en unicode en emoji

    async def __init__(self, obj: object, ctx: commands.Context, *,
    role=False,
    task=False,
    user=False,

    title='Titulo',
    description='Descripcion',
    ):
        self.obj = obj
        self.disc_obj: object
        self.ctx = ctx
        self.title = title
        self.description = description

        self._role = role
        self._task = task
        self._user = user
        
        self._atributes_dic = self.obj.__dict__.copy()
        self._things_list: dict
        self._embed: discord.Embed

        self.channel = ctx.author.dm_channel 
        if not self.channel:
            self.channel = self.ctx.author.create_dm()


    async def modify(self):
        '''Ejecuta la conversacion en el modo `"modify"`'''

        await self._conversate(mode='modify')

    async def create(self):
        '''Ejecuta la conversacion en el modo `"create"`'''

        await self._conversate(mode='modify')




    def _values_for_new_class(self):
        '''Actualiza `title` y `description` para el mensaje `discord.Embed` en el modo `"create"`'''

        self.title = self.obj._newtitle(self.ctx)
        self.description = self.obj._new_desc(self.ctx)

    def _values_for_mod_class(self):
        '''Actualiza `title` y `description` para el mensaje `discord.Embed` en el modo `"modify"`'''

        self.title = self.obj._modtitle(self.ctx)
        self.description = self.obj._mod_desc(self.ctx)
    



    def _prepare_disc_obj(self):
        '''Esta funcion se debe modificar si se quieren introducir nuevas clases modificables'''

        if self._role:
            disc_obj = ctx.guild.get_role(obj.id)
        elif self._task:
            disc_obj = obj
        elif self._user:
            disc_obj = ctx.guild.get_member(obj.id)

    def _save_obj(self):
        '''Esta funcion se debe modificar si se quieren introducir nuevas clases modificables'''

        if self._role:
            self.obj.database.update_rol(self.obj)
        elif self._task:
            self.obj.database.update_task(self.obj)
        elif self._user:
            self.obj.database.update_user(self.obj)


    def _prepare_dicts(self):
        '''Prepara los diccionarios internos para trabajar con ellos'''

        self._atributes_dic.pop('id')
        self._atributes_dic.pop('database')
        try:
            self._atributes_dic.pop('mention')
        except KeyError:
            pass

        self._things_list = {f"{chr(i)}": v for i, v in enumerate(self._atributes_dic, start=self.CODEPOINT_START)}


    def _create_embed(self) -> discord.Embed:
        '''Crea la cabecera del mensaje `discord.Embed` y lo devuelve para escritura dinamica'''

        self._embed = discord.Embed(
            title=self.title,
            description=self.description,
            color=discord.Color.dark_green()
        )
        return self._embed


    def _re_embed(self) -> discord.Embed:
        '''Actualiza el `discord.Embed` de la clase y lo devuelve para eescritura dinamica'''

        self._embed.clear_fields()
        for atrib in self._things_list:
            self._embed.add_field(
                name=f"{atrib} - {self._things_list[atrib]}:",
                value=obj.__dict__[self._things_list[atrib]],
                inline=False
                )
        return self._embed


    def embed(self) -> discord.Embed:
        '''Devuelve el mensaje tipo `discord.Embed`. Si no esta creado lo crea, y si lo esta lo actualiza'''

        if not self._embed:
            self._embed = self._create_embed()
        else: 
            self._re_embed()
        return self._embed


    async def _add_reactions(self, message):
        '''Añade las reacciones necesarias al `discord.Message`'''

        for i in range(len(self._things_list)):
            await message.add_reaction(chr(i+self.CODEPOINT_START)) 
        await message.add_reaction("💾")
    

    async def dm_send(self, *, text='') -> discord.Message:
        '''Envia un `discord.Message` al usuario a traves del `discord.DMChannel`. 
        Por defecto envia un `discord.Embed`. Si se especifica `text` se envia eso'''

        if text:
            return await self.channel.send(text)
        else:
            return await self.channel.send(embed=self.embed())


    async def dm_resend(self, message):
        '''Edita el `discord.Message` dado con el `discord.Embed` actualizado'''

        return await message.edit(embed=self.embed())


    async def ctx_send(self) -> discord.Message:
        '''Envia un mensaje al contexto que inicio el comando con el `discord.Embed` actual'''

        return await self.ctx.send(embed=self.embed())


    async def _time_out(self) -> bool:
        '''Envia un mensaje por el canal `dicord.DMChannel` informando de la llegada al limite de tiempo'''

        await self.channel.send('Se acabo el tiempo...')
        return False


    

    
    async def _conversate(self, *, mode='create'):
        '''Conversacion que permite modificar a tiempo real los valores de `obj` con un `discord.Embed`'''

        self._prepare_dicts()
        self._prepare_disc_obj()

        if mode == 'create':
            self._values_for_new_class()
        if mode == 'modify':
            self._values_for_mod_class()

        self.embed()

        message = await self.dm_send()
        await self._add_reactions(message)


        async def _ask_field() -> bool:
            '''Esta funcion se encarga de preguntar una y otra vez si se quiere cambiar algun campo y cual'''

            await self.dm_resend(message)

            try:
                reaction, user = await ctx.bot.wait_for('reaction_add', timeout=30.0)
                if str(reaction.emoji) == '💾':
                    return False
                    
            except asyncio.TimeoutError:
                return await self._time_out()

            ask_message = await channel.send(f"Introduce un nuevo {self._things_list[reaction.emoji]}:")

            try:
                response_msg = await ctx.bot.wait_for('message', timeout=150.0)
            except asyncio.TimeoutError:
                return await self._time_out()
            
            setattr(self.obj, self._things_list[reaction.emoji], response_msg.content)
            await response_msg.add_reaction("✅")
            await ask_message.delete()
            return True
        

        while await self._conversate._ask_field():
            pass
        await self._re_embed()

        self._save_obj()