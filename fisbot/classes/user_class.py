import math
import random
import time
from random import randint

import discord

from ..database import users
from .achievements_class import Achievements
from .display_class import *
from .rol_class import FisRol

import logging

class FisUser(Display):

    C = 0.001

    _title_for_mod = 'Modificar **{0.name}**'
    _title_for_del = 'Eliminar **{0.name}** de la base de datos'

    _descr_for_mod ='''Abajo tienes la lista de todos los campos modificables. 
        Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
        *Cuando hayas acabado* presiona el boton de guardar'''
    _descr_for_del ='''¿Seguro que quiere eliminar este elemento de la base de datos?
        Si es así, reaccione ✅. De lo contrario, reaccione ❌:'''

    def __init__(self, user_id=0, name='', karma=0, level=0, xp=0, last_message=None, last_join=time.time(), cromos=''):
        self.id = int(user_id)
        self.name = name
        self.karma = int(karma if karma else 0) 
        self.level = int(level if level else 0)
        self.xp = int(xp if xp else 0)
        self.last_message = float(last_message if last_message else time.time())
        self.last_join = float(last_join if last_join else time.time())
        try:
            self.cromos = list(map(int, cromos.split()))
        except AttributeError:
            self.cromos = []


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


    async def level_up(self, bot, guild):
        '''ASYNC Te sube de nivel'''

        mention = f"<@{self.id}>"
        level = self.level

        with open(f".{bot.BOT_PATH}/fisbot/database/celebrations.txt", 'r', encoding='utf8') as file:
            lines = file.readlines()
            line = lines[randint(0, len(lines)-1)]

            if guild.system_channel:
                buff = 'f"""'+line+'"""'
                buff = eval(buff, locals())
                await guild.system_channel.send(buff)

        try:
            roles_nuevos = FisRol.check_new_rol_needed(self)
            if not roles_nuevos:
                return
        
            try:
                for role in roles_nuevos:
                    guild = bot.get_guild(role.guild_id)
                    try:
                        await role.give_to(self, guild=guild)
                    except:
                        pass
            except:
                pass

            roles_previos = FisRol.prev_roles_of_level(self.level)
            if roles_previos:
                try:
                    for rol in roles_previos:
                        await rol.remove_from(self, guild=bot.get_guild(rol.guild_id))
                except:
                    pass
        except Exception as e:
            logging.error(e)
            pass

    async def addxp(self, bot, guild, *, amount=1, time=0, amount_type='Text') :
        '''ASYNC Sube la experiencia del usuario. Si el usuario necesita subir de nivel, lo hace'''

        if amount_type == 'Text':
            x = self.C*time**2
            t = 40*self.level/(160-8*self.level+0.2*self.level**2)+20
            h = x/(1+x)

        if amount_type == 'Voice':
            if self.level<20:
                t = 20*self.level/(320-2*self.level+0.8*self.level**2) + 1
            else:
                t = 11*self.level**2/(600-self.level+0.8*self.level**2) + 1
            h = time/3600

        amount *= self.xp_to_lvl_up()/t*h

        newxp = self.xp + amount
        xp_required = self.xp_to_lvl_up()
        self.xp = newxp
        while self.xp >= xp_required:
            self.xp -=  xp_required
            self.level += 1
            await self.level_up(bot, guild)  
        await self.save_in_database()


    @classmethod
    def last_message_cooldown(cls, user_id):
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
    

    def embed_show_crome(self, n):
        embed = discord.Embed(
            title=f'Cromos de {self.name}:',
            color=discord.Color.blue()
        )
        with open('cromos.txt', 'r') as file:
            for i in range(n):
                file.readline()
            return embed.set_image(url=file.readline())


    async def embed_show(self) -> discord.Embed:
        '''ASYNC Devuelve un mensaje tipo `discord.Embed` que muestra la info del usuario'''

        await self.discord_obj()
        ach = Achievements.get_achievement(self)
        try:
            if self.name != self._disc_obj.nick:
                self.name = self._disc_obj.display_name
                await self.save_in_database()
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
        embed.set_thumbnail(url=str(self._disc_obj.avatar.replace(size=256)))
        return embed