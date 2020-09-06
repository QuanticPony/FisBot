import discord
import asyncio
import functools
from discord.ext import commands

class Display():

    CODEPOINT_START = 127462

    async def __init__(self, ctx: commands.Context, *,
    title='Titulo',
    description='Descripcion',
    ):
        self._ctx = ctx
        self._title = title
        self._description = description

        self._disc_obj = self.discord_obj()
        
        self._atributes_dic = self.__dict__.copy()
        self._things_list: dict
        self._embed: discord.Embed

        self._channel = ctx.author.dm_channel 
        if not self._channel:
            self._channel = self._ctx.author.create_dm()


# DECORADORES: prepara los diccionarios internos

    def prepare_dicts(funcion):
        '''Decorador que prepara los elementos de los diccionarios'''

        @functools.wraps(funcion)
        def decorator(self, *args, **kargs):
            self.prepare_atributes_dic()
            self._prepare_elements()
            funcion(*args, **kargs)
        return decorator

# DECORADORES: checks

    def check_if_discord_obj(funcion):
        '''Debe ser utilizado cuando se necesita el objeto de discord relacionado.
        Llama a la funcion sobreescrita `discord_obj()`'''

        @functools.wraps(funcion)
        def decorator(self, *args, **kargs):
            if not self._disc_obj:
                self.discord_obj()
            funcion(*args, **kargs)
        return decorator


    def check_if_context(funcion):
        '''Debe ser utilizada siempre que se quiera acceder a algo del servidor.
        Comprueba que el atributo `_ctx` es un objeto de tipo `commands.Context`'''

        @functools.wraps(funcion)
        def decorator(self, *args, **kargs):
            if isinstance(self._ctx, commands.Context):
                funcion(*args, **kargs)
        return decorator

    def check_if_channel(funcion):
        '''Debe ser utilizada siempre que se quiera enviar un mensaje al usuario por privado.
        Comprueba que el atributo `_channel` es un objeto de tipo `discord.DMChannel`'''

        @functools.wraps(funcion)
        def decorator(self, *args, **kargs):
            if isinstance(self._channel, discord.DMChannel):
                function(*args, **kargs)
        return decorator



    # No modificar estas funciones en esta clase 
# Sobreescribir las funciones en clases que hereden de esta

    async def embed_show(self) -> discord.Embed: ... # Debe devolver un mensaje tipo discord.Embed que muestre el objeto

    async def discord_obj(self) -> object:... # Debe devolver el objeto similar de discord
    async def save_in_database(self):... # Debe guardar el objeto en la base de datos
    async def remove_from_database(self):... # Debe eliminar el objeto de la base de datos

    async def title_for_new(self) -> str:... # Debe devolver el titulo del display en la opcion de crear
    async def title_for_mod(self) -> str:... # Debe devolver el titulo del display en la opcion de modificar  
    async def title_for_del(self) -> str:... # Debe devolver el titulo del display en la opcion de borrar

    async def description_for_new(self) -> str:... # Debe devolver la descripcion del display en la opcion de crear
    async def description_for_mod(self) -> str:... # Debe devolver la descripcion del display en la opcion de modificar
    async def description_for_del(self) -> str:... # Debe devolver la descripcion del display en la opcion de borrar

    def prepare_atributes_dic(self):... # Prepara el diccionario _atributes_dic con los elementos que se permite modificar      

# Funciones que hay que llamar

    async def create(self):
        '''Ejecuta la conversacion en el modo `"create"`'''

        await self._conversate(mode='create')

    async def modify(self):
        '''Ejecuta la conversacion en el modo `"modify"`'''

        await self._conversate(mode='modify')

    async def delete(self):
        '''Ejecuta la conversacion en el modo `"delete"`'''

        await self._conversate(mode='delete')

# Titulo y descripcion

    @prepare_dicts
    async def _values_for_new_class(self):
        '''Actualiza `title` y `description` para el mensaje `discord.Embed` en el modo `"create"`'''

        self._title = await self.title_for_new()
        self._description = await self.description_for_new()
        
    @prepare_dicts
    async def _values_for_mod_class(self):
        '''Actualiza `title` y `description` para el mensaje `discord.Embed` en el modo `"modify"`'''

        self._title = await self.title_for_mod()
        self._description = await self.description_for_mod()
    
    async def _values_for_del_class(self):
        '''Actualiza `title` y `description` para el mensaje `discord.Embed` en el modo `"delete"`'''

        self._title = await self.title_for_del()
        self._description = await self.description_for_del()
        self.embed()
        self._embed += f"\n ✅ - **Eliminar** \n ❌ - **Cancelar**"
        self._things_list = ['✅','❌']

# Elementos

    def _prepare_elements(self):
        '''Quitamos todos los atributos que no este permitido modificar: los que empiezan por `_`.
        Y crea el diccionario `_things_list`'''

        for key in self._atributes_dic:
            if key.startswith('_'):
                self._atributes_dic.pop(key) 

        self._things_list = {f"{chr(i)}": v \
            for i, v in enumerate(self._atributes_dic, start=self.CODEPOINT_START)}


# Embeds

    def _create_embed(self) -> discord.Embed:
        '''Crea la cabecera del mensaje `discord.Embed` y lo devuelve para escritura dinamica'''

        self._embed = discord.Embed(
            title=self._title,
            description=self._description,
            color=discord.Color.dark_green()
        )
        return self._embed


    def _re_embed(self) -> discord.Embed:
        '''Actualiza el `discord.Embed` de la clase y lo devuelve para escritura dinamica'''

        self._embed.clear_fields()
        for atrib in self._things_list:
            self._embed.add_field(
                name=f"{atrib} - {self._things_list[atrib]}:",
                value=self.__dict__[self._things_list[atrib]],
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

        if self._embed._fields:
            for i in range(len(self._things_list)):
                await message.add_reaction(chr(i+self.CODEPOINT_START)) 
            await message.add_reaction('💾')
        else:
            await message.add_reaction('✅')
            await message.add_reaction('❌')
    
# Mensajes

    @check_if_channel
    async def dm_send(self, *, text='') -> discord.Message:
        '''Envia un `discord.Message` al usuario a traves del `discord.DMChannel`. 
        Por defecto envia un `discord.Embed`. Si se especifica `text` se envia eso'''

        if text:
            return await self._channel.send(text)
        else:
            return await self._channel.send(embed=self.embed())


    async def resend(self, message):
        '''Edita el `discord.Message` dado con el `discord.Embed` actualizado'''

        return await message.edit(embed=self.embed())


    @check_if_context
    async def ctx_send(self) -> discord.Message:
        '''Envia un mensaje al contexto que inicio el comando con el `discord.Embed` actual'''

        return await self._ctx.send(embed=self.embed())

    @check_if_channel
    async def _time_out(self) -> bool:
        '''Envia un mensaje por el canal `dicord.DMChannel` informando de la llegada al limite de tiempo'''

        await self._channel.send('Se acabo el tiempo...')
        return False

# Conversacion

    @check_if_channel
    @check_if_context
    async def _conversate(self, *, mode='create'):
        '''Conversacion que permite modificar a tiempo real los valores del objeto con un `discord.Embed`'''

        actualice_values = {
            'create': await self._values_for_new_class(),
            'modify': await self._values_for_mod_class(),
            'delete': await self._values_for_del_class()
        }
        actualice_values[mode]
        
        message = await self.dm_send()
        await self._add_reactions(message)

        async def _ask_field() -> bool:
            '''Esta funcion se encarga de preguntar una y otra vez si se quiere cambiar algun campo y cual'''

            await self.dm_resend(message)

            try:
                reaction, user = await self._ctx.bot.wait_for('reaction_add', timeout=30.0)
                if str(reaction.emoji) == '💾':
                    self.save_in_database()
                    return False

                elif str(reaction.emoji) == '✅':
                    self.remove_from_database()
                    return False
                    
                elif str(reaction.emoji) == '❌':
                    return False

            except asyncio.TimeoutError:
                return await self._time_out()

            ask_message = await self.dm_send(f"Introduce un nuevo {self._things_list[reaction.emoji]}:")

            try:
                response_msg = await self._ctx.bot.wait_for('message', timeout=150.0)
            except asyncio.TimeoutError:
                return await self._time_out()
            
            setattr(self, self._things_list[reaction.emoji], response_msg.content)
            await response_msg.add_reaction("✅")
            await ask_message.delete()
            return True

        while await self._conversate._ask_field():
            pass