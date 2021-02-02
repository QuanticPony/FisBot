import random
import math
import discord
import time
from random import randint
from .rol_class import FisRol
from .display_class import *
from ..database import users

class FisUser(Display):

    XP_ADD_BASE = 6

    _title_for_mod = 'Modificar **{0.name}**'
    _title_for_del = 'Eliminar **{0.name}** de la base de datos'

    _descr_for_mod ='''Abajo tienes la lista de todos los campos modificables. 
        Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
        *Cuando hayas acabado* presiona el boton de guardar'''
    _descr_for_del ='''¿Seguro que quiere eliminar este elemento de la base de datos?
        Si es así, reaccione ✅. De lo contrario, reaccione ❌:'''

    def __init__(self, user_id=0, name='', karma=0, level=0, xp=0, last_message=0, last_join=time.time()):
        self.id = int(user_id)
        self.name = name
        self.karma = int(karma)
        self.level = int(level)
        self.xp = int(xp)
        self.last_message = int(last_message)
        self.last_join = last_join


    @classmethod
    def convert_from_database(cls, funcion, *args):
        '''Ejecuta la funcion `funcion` con los argumentos dados en la base de datos. Convierte el resultado a un
        objeto FisUser'''

        try:
            result = [cls(*line) for line in funcion(*args)]
        except:
            result = None
        return result


    @classmethod
    async def init_with_member(cls, member: discord.Member, *, context=None):
        '''ASYNC Devuelve un usuario `FisUser` a partir de un miembro'''

        user = cls.convert_from_database(users.UsersDB.get_user, member.id)
        if not user:
            user = cls(user_id=member.id, name=member.display_name)
            users.UsersDB.add_user(user)

        if context:
            await user.init_display(context)
        return user

    def title_for_mod(self) -> str:

        return self._title_for_mod.format(self)

    def title_for_del(self) -> str:
        return self._title_for_del.format(self)


    def description_for_mod(self) -> str:

        return self._descr_for_mod.format(self)

    def description_for_del(self) -> str:

        return  self._descr_for_del.format(self)


    def xp_to_lvl_up(self) -> int:
        '''Devuelve la cantidad de experiencia necesaria para subir al siguiente nivel'''
        
        return ((self.level ** 2) + self.level + 2) * 50 - self.level * 100


    # TODO: preguntar a Aitor como puedo optimizar esta función para no crear el diccionario cada vez que alguien sube de nivel
    async def level_up(self, bot, guild):
        '''ASYNC Te sube de nivel'''

        mention = lambda: f"<@{self.id}>"
        new_level_frases = {
                    0: f"Buena {mention()}!! Alguien ha subido al nivel {self.level}...",
                    1: f"{mention()} ha ascendido al nivel {self.level}!! Esperemos que no se le suba a la cabeza...",
                    2: f"Felicidades {mention()}!! Disfruta de tu nivel {self.level}!",
                    3: f"Ya falta poco! Dentro de tan solo {1000-self.level} te damos rango admin {mention()}!",
                    4: f"**Dato curioso**: Los koalas bebes lamen el ano de sus madres. Y {mention()} es tan solo nivel {self.level}",
                    5: f"**Dato curioso**: 0.7% de la poblacion mundial se encuentra permanentemente borracha. Y {mention()} es nivel {self.level}",
                    6: f"**Dato curioso**: Un **144%** de los datos que te encuentras en internet son ||FALSOS||. Y {mention()} ha subido a nivel {self.level**2 * 86}"
                }

        if guild.system_channel:
            await guild.system_channel.send(new_level_frases[randint(0,len(new_level_frases) - 1)])

        roles_nuevos = FisRol.check_new_rol_needed(self)
        if not roles_nuevos:
            return
        
        for role in roles_nuevos:
            guild = bot.get_guild(role.guild_id)

            if guild and self._disc_obj in guild.members:
                await role.give_to(self, guild=guild)

                roles_previos = FisRol.prev_roles_of_level(self.level)
                if roles_previos:
                    for rol in roles_previos:
                        await rol.remove_from(self, guild=bot.get_guild(rol.guild_id))


    async def addxp(self, bot, guild, *, amount=None) :
        '''ASYNC Sube la experiencia del usuario. Si el usuario necesita subir de nivel, lo hace'''
        
        if not amount:
            amount = random.randint(1, self.XP_ADD_BASE) * (random.randint(1, self.level+1) if self.level > 0 else 1)

        newxp = self.xp + amount
        xp_required = self.xp_to_lvl_up()
        self.xp = newxp
        if self.xp >= xp_required:
            self.xp -=  xp_required
            self.level += 1
            await self.level_up(bot, guild)  
        users.UsersDB.update_user(self)

    @check_if_context()
    async def discord_obj(self) -> discord.Member:
        '''ASYNC Devuelve el objeto de discord asociado: `discord.Member` si lo encuentra en el 
        servidor del contexto. Si no lo encuentra devuelve `None`'''

        try:
            # TODO: comprobar esto
            self._disc_obj = self._ctx.guild.get_member(self.id)
            #self._disc_obj = self._ctx.guild.get_member_named(self.name)
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
        
        return users.UsersDB.update_user(self)

    async def remove_from_database(self):
        '''ASYNC Elimina al usuario en la base de datos. Devuelve `True` si lo ha conseguido y `False` si no '''

        return users.UsersDB.del_user(self)

    def prepare_atributes_dic(self):
        '''Prepara los diccionarios internos para trabajar con ellos'''

        self._atributes_dic = self.__dict__.copy()

        for key in ['id', 'name', 'database', 'last_message', 'last_join']:
            try:
                self._atributes_dic.pop(key)
            except KeyError:
                continue


    # TODO: Hay que rehacer esto
    async def embed_show(self) -> discord.Embed:
        '''ASYNC Devuelve un mensaje tipo `discord.Embed` que muestra la info del usuario'''

        await self.discord_obj()

        embed= discord.Embed(
            title=self.name if self.name else self._disc_obj.name,
            color=discord.Color.green()
        )
        if self._disc_obj:
            embed.description= 'Nombre en discord: ' + self._disc_obj.name
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