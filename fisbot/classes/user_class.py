import math
import random
import time
from random import randint

import discord

from ..database import users
from .achievements_class import Achievements
from .display_class import *
from .rol_class import FisRol


class FisUser(Display):

    C = 0.001

    _title_for_mod = 'Modificar **{0.name}**'
    _title_for_del = 'Eliminar **{0.name}** de la base de datos'

    _descr_for_mod ='''Abajo tienes la lista de todos los campos modificables. 
        Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
        *Cuando hayas acabado* presiona el boton de guardar'''
    _descr_for_del ='''¿Seguro que quiere eliminar este elemento de la base de datos?
        Si es así, reaccione ✅. De lo contrario, reaccione ❌:'''

    def __init__(self, user_id=0, name='', karma=0, level=0, xp=0, last_message=None, last_join=time.time()):
        self.id = int(user_id)
        self.name = name
        self.karma = int(karma if karma else 0) 
        self.level = int(level if level else 0)
        self.xp = int(xp if xp else 0)
        self.last_message = last_message
        self.last_join = last_join


    def __eq__(self, value):
        if isinstance(value, FisUser):
            return self.id == value.id
        else:
            return False


    @classmethod
    def convert_from_database(cls, funcion, *, args=[]):
        '''Ejecuta la funcion `funcion` con los argumentos dados en la base de datos. Convierte el resultado a un
        objeto FisUser'''

        if args:
            _return = funcion(args)
        else: 
            _return = funcion()

        try:
            
            result = cls(*_return)
        except:
            try:
                result = [cls(*line) for line in funcion(*args)]
            except:
                return None
        return result


    @classmethod
    async def init_with_member(cls, member: discord.Member, *, context=None):
        '''ASYNC Devuelve un usuario `FisUser` a partir de un miembro'''

        user = cls.convert_from_database(users.UsersDB.get_user, args=member.id)
        
        if not user:
            user = cls(user_id=member.id, name=member.display_name)
            users.UsersDB.add_user(user)
        user.name = member.display_name

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

        # TODO: rehacer esto

        if guild.system_channel:
            await guild.system_channel.send(new_level_frases[randint(0,len(new_level_frases) - 1)])

        roles_nuevos = FisRol.check_new_rol_needed(self)
        if not roles_nuevos:
            return

        try:
            for role in roles_nuevos:
                guild = bot.get_guild(role.guild_id)
                if guild and self._disc_obj in guild.members:
                    await role.give_to(self, guild=guild)
        except:
            pass
        

        roles_previos = FisRol.prev_roles_of_level(self.level)
        if roles_previos:
            try:
                for rol in roles_previos:
                    await rol.remove_from(self, guild=bot.get_guild(rol.guild_id))
            except:
                pass

    async def addxp(self, bot, guild, *, amount=None, time=0, amount_type='Text') :
        '''ASYNC Sube la experiencia del usuario. Si el usuario necesita subir de nivel, lo hace'''

        if not amount:
            with self.level as l:
                if amount_type is 'Text':
                    with self.C*time^2 as x:
                        t = x/(1+x)
                        h = 80*self.level/(160-8*l+0.2*l^2)+20


                if amount_type is 'Voice':
                    t = 80*self.level/(320-8*l+l^2)+1
                    h = time/3600

            amount = self.xp_to_lvl_up()/t * h

        newxp = self.xp + amount
        xp_required = self.xp_to_lvl_up()
        self.xp = newxp
        if self.xp >= xp_required:
            self.xp -=  xp_required
            self.level += 1
            await self.level_up(bot, guild)  
        users.UsersDB.update_user(self)


    @classmethod
    def last_message_cooldown(cls, user_id)-> (float, list):
        '''Comprueba si la llamada a esta funcion y con la ultima llamada a la misma del mismo `user_id` es mayor que el cooldown.
        Devuelve un float que es la cantidad de tiempo desde el ultimo mensaje del usuario de la base de datos con mismo id'''

        now_time = time.time()
        if user_id:
            user = cls.convert_from_database(users.UsersDB.get_user, args=user_id) 
            if user:
                users.UsersDB.execute('UPDATE Users SET last_message = ? WHERE id = ?', args=(now_time, user_id))
                if not user.last_message:
                    user.last_message = now_time-1000
                
                    
                return (now_time-user.last_message, user)
        return (1000, user)
    

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

        
    def get_achievements(self):
        return Achievements.get_achievement(self)


    async def embed_show(self) -> discord.Embed:
        '''ASYNC Devuelve un mensaje tipo `discord.Embed` que muestra la info del usuario'''

        await self.discord_obj()
        ach = Achievements.get_achievement(self)
        try:
            if self.name != self._disc_obj.nick:
                self.name = self._disc_obj.nick
                self.save_in_database()
        except:
            pass

        embed= discord.Embed(
            title=self.name,
            color=discord.Color.from_rgb(*(ach.color))
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

        frase = ''
        if ach.extras:
            frase += ach.extras + '\n'

        
        for moment, level in ach.level_s_y:
            try:
                frase += f"{moment.replace('_', ' ',2).replace('_','-')}: Nivel {level}\n" if level > 4 else ''
            except:
                pass
        
        if frase:
            embed.add_field(
                name='Logros:',
                value=frase,
                inline=False
            )
        embed.set_thumbnail(url=str(self._disc_obj.avatar_url_as(size=256)))
        return embed