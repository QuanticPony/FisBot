from ..classes.user_class import FisUser
from .base import database
import sqlite3
from sqlite3 import Connection
import time

class UsersDB(database):

    COOLDOWN = 15

    SQL_TABLE ='''CREATE TABLE IF NOT EXISTS Users (
        id text NOT NULL PRIMARY KEY,
        name text,
        karma integer,
        level integer,
        xp integer,
        last_message,
        last_join
        )'''
    
    @classmethod
    def add_user(cls, user: FisUser) -> bool:
        '''Añade un usuario a la base de datos. Si el usuario se ha añadido devuelve True,
        en caso contrario (si ya existe uno con el mismo id) devuelve `False`.'''

        if not isinstance(user, FisUser):
            return False
        try:
            with cls._connect() as conn:
                c = conn.cursor()
                c.execute('INSERT INTO Users VALUES (?,?,?,?,?,?,?)', 
                    (user.id, user.name, user.karma, user.level, user.xp, user.last_message, user.last_join))
            return True
        except sqlite3.IntegrityError:
            return False
    
    @classmethod
    def update_user(cls, user: FisUser) -> bool:
        '''Actualiza los datos de un usuario si existe en la base de datos. Si el usuario
        existe y se ha podido modificar devuelve `True`, en caso contrario devuelve `False`.'''

        if not isinstance(user, FisUser):
            return False
        try:
            with cls._connect() as conn:
                c = conn.cursor()
                c.execute('UPDATE Users SET name = ?, karma = ?, level = ?, xp = ? WHERE id = ?', 
                    (user.name, user.karma, user.level, user.xp, user.id))
            return True
        except sqlite3.Error:
            return False
    
    @classmethod
    def del_user(cls, user: FisUser) -> bool:
        '''Elimina un usuario de la base de datos si su id coincide con el de `user`. 
        Si el usuario se ha eliminado devuelve `True`, en caso contrario devuelve `False`.'''

        if not isinstance(user, FisUser):
            return False
        try:
            with cls._connect() as conn:
                c = conn.cursor()
                c.execute('DELETE FROM Users WHERE id = ?', (user.id,))
            return True
        except sqlite3.Error:
            return False
    
    @classmethod
    def get_user(cls, user_id) -> FisUser:
        '''Obtiene un usuario de la base de datos si su id coincide con `user_id`.
        Si el usuario no se encuentra devuelve `None`.'''

        if not user_id:
            return False
        with cls._connect() as conn:
            c = conn.cursor()
            try:
                result = c.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
            except sqlite3.Error:
                return None
            if not result:
                cls.add_user(FisUser(user_id))
                return None
        return FisUser(*result)
    
    @classmethod
    def get_all_users(cls) -> tuple:
        '''Devuelve una colección de todos los usuarios registrados en la base de datos
        ordenados alfabéticamente.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Users ORDER BY name').fetchall()
        except sqlite3.Error:
            return None
        return tuple([FisUser(*user) for user in result])

    @classmethod
    def last_message_cooldown(cls, user_id)-> (bool, FisUser):
        '''Comprueba si la llamada a esta funcion y con la ultima llamada a la misma del mismo `user_id` es mayor que el cooldown.
        Devuelve un booleano si cumple el cooldown y el usuario de la base de datos con mismo id'''

        now_time = time.time()
        if user_id:
            try:
                with cls._connect() as conn:
                    c = conn.cursor()
                    last_time , = c.execute('SELECT last_message FROM Users WHERE id = ?', (user_id,)).fetchone()
                    user = cls.get_user(user_id)
                    if user:
                        c.execute('UPDATE Users SET last_message = ? WHERE id = ?', (now_time, user_id))
            except sqlite3.Error:
                return (False, None)

            if not last_time:
                return (True, user)
            if now_time - last_time >= cls.COOLDOWN:
                return (True, user)
        return (False, None)

    @classmethod
    def new_voice_join(cls, user_id):
        '''Permite ingresar el momento en el que el usuario de id especificada se conecto a un canal de voz por ultima vez.
        Devuelve `True` si lo ha conseguido actualizar en la base de datos'''

        now_time = time.time()
        if not user_id:
            return False
        try:
            with cls._connect() as conn:
                c = conn.cursor()
                c.execute('UPDATE Users SET last_join = ? WHERE id = ?', (now_time, user_id))
                return True
        except sqlite3.Error:
            return False

    @classmethod
    def last_voice_join(cls, user_id)-> (bool, FisUser):
        '''Devuelve la hora en la que se conecto el usuario por ultima vez.
        Devuelve el usuario de la base de datos con mismo id'''

        now_time = time.time()
        if user_id:
            try:
                with cls._connect() as conn:
                    c = conn.cursor()
                    last_time , = c.execute('SELECT last_join FROM Users WHERE id = ?', (user_id,)).fetchone()
                    user = cls.get_user(user_id)
                    if user:
                        c.execute('UPDATE Users SET last_join = ? WHERE id = ?', (now_time, user_id))
            except sqlite3.Error:
                return (False, None)

            return (now_time - last_time, user)
        return (False, None)

