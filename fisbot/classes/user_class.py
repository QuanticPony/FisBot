import random
import math
import discord
import time
from random import randint
from .rol_class import FisRol
from .display_class import *

class FisUser(Display):

    XP_ADD_BASE = 6

    _title_for_mod = 'Modificar **{0.subject}**: *{0.title}*'

    _descr_for_mod ='''Abajo tienes la lista de todos los campos modificables. 
        Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
        *Cuando hayas acabado* presiona el boton de guardar'''

    def __init__(self, user_id=0, name='', karma=0, level=0, xp=0, last_message=0, last_join=None):
        self.id = int(user_id)
        self.name = name
        self.karma = int(karma)
        self.level = int(level)
        self.xp = int(xp)
        self.last_message = int(last_message)
        if not last_join:
            last_join = time.time()
        self.last_join = last_join

        from ..database.users import UsersDB
        self.database = UsersDB

    @classmethod
    async def init_with_member(cls, member: discord.Member, *, context=None):
        '''ASYNC Devuelve un usuario `FisUser` a partir de un miembro'''

        user = cls().database.get_user(member.id)
        if not context:
            return user
        else:
            await user.init_display(context)
            return user

    def _mod_title(self) -> str:
        '''Devuelve el titulo utilizado en la modificacion de esta clase'''

        return f"Modificar usuario id={self.id}"
    
    def _mod_desc(self) -> str:
        '''Devuelve la descripcion utilizada en la modificacion de esta clase'''

        return '''Abajo tienes la lista de todos los campos modificables. 
    Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
    *Cuando hayas acabado* presiona el boton de guardar'''



    def xp_to_lvl_up(self) -> int:
        '''Devuelve la cantidad de experiencia necesaria para subir al siguiente nivel'''
        
        return ((self.level ** 2) + self.level + 2) * 50 - self.level * 100

    async def level_up(self, guild):
        '''ASYNC Te sube de nivel'''

        mention = lambda: f"<@{self.id}>"
        new_level_frases = {
                    0: f"Buena {mention()}!! Alguien ha subido al nivel {self.level}...",
                    1: f"{mention()} ha ascendido al nivel {self.level}!! Esperemos que no se le suba a la cabeza...",
                    2: f"Felicidades {mention()}!! Disfruta de tu nivel {self.level}!",
                    3: f"Ya falta poco! Dentro de tan solo {1000-self.level} te damos rango admin {mention()}!",
                    4: f"**Dato curioso**: Los koalas bebes lamen el ano de sus madres. Y {mention()} es tan solo nivel {self.level}"
                }
        await guild.system_channel.send(new_level_frases[randint(0,len(new_level_frases) - 1)])

        rol = FisRol().check_new_rol_needed(self)
        if rol:
            await rol.give_to(self, guild=guild)
            rol = rol.prev_role_of_level(self.level)
            if rol:
                await rol.remove_from(self, guild=guild)

    async def addxp(self, guild, amount=None) :
        '''ASYNC Sube la experiencia del usuario. Si el usuario necesita subir de nivel, lo hace'''
        
        if not amount:
            amount = random.randint(1, self.XP_ADD_BASE) * (random.randint(1, self.level+1) if self.level > 0 else 1)

        newxp = self.xp + amount
        xp_required = self.xp_to_lvl_up()
        if newxp >= xp_required:
            self.xp = newxp - xp_required
            self.level += 1
            await self.level_up(guild)
            self.database.update_user(self)
        else:
            self.xp = newxp
            self.database.update_user(self)

    @check_if_context()
    async def discord_obj(self) -> discord.Member:
        '''ASYNC Devuelve el objeto de discord asociado: `discord.Member` si lo encuentra en el 
        servidor del contexto. Si no lo encuentra devuelve `None`'''

        try:
            self._disc_obj = self._ctx.guild.get_member(self.id)
        except:
            self._disc_obj = None
        return self._disc_obj

    @check_if_context()
    async def update_discord_obj(self):
        '''ASYNC Modifica el nombre del usuario en discord y devuelve `True`. Si hay algún problema devuelve `False`'''
        
        try:
            if isinstance(self._disc_obj, (discord.User, discord.Member)):
                return
            await self._disc_obj.edit(nick=self.name)
            return True
        except:
            return False

    async def save_in_database(self) -> bool:
        '''ASYNC Guarda al usuario en la base de datos. Devuelve `True` si lo ha conseguido y `False` si no '''
        
        return self.database.update_user(self)

    async def remove_from_database(self):
        '''ASYNC Elimina al usuario en la base de datos. Devuelve `True` si lo ha conseguido y `False` si no '''

        return self.database.del_user(self)

    def prepare_atributes_dic(self):
        '''Prepara los diccionarios internos para trabajar con ellos'''

        self._atributes_dic = self.__dict__.copy()

        for key in ['id', 'name', 'database', 'last_message', 'last_join']:
            try:
                self._atributes_dic.pop(key)
            except KeyError:
                continue

    async def embed_show(self) -> discord.Embed:
        '''ASYNC Devuelve un mensaje tipo `discord.Embed` que muestra la info del usuario'''

        await self.discord_obj()

        embed= discord.Embed(
            title=self.name if self.name else self._disc_obj.name,
            description='Nombre en discord: ' + self._disc_obj.name,
            color=discord.Color.green()
        )
        embed.add_field(
            name='Nivel:',
            value=self.level,
            inline=True
        )
        embed.add_field(
            name='Experiencia:',
            value=f"{self.xp}/{self.xp_to_lvl_up()}",
            inline=True
        )
        embed.add_field(
            name='Karma:',
            value=self.karma,
            inline=True
        )
        embed.set_thumbnail(url=str(self._disc_obj.avatar_url_as(size=128)))
        return embed