from ..classes.user_class import FisUser
from .base import database
import sqlite3
from sqlite3 import Connection
import time

class UsersDB(database):

    SQL_TABLE ='''CREATE TABLE IF NOT EXISTS Users (
        id text NOT NULL PRIMARY KEY,
        name text,
        karma integer,
        level integer,
        xp integer
        )'''
    
    @classmethod
    def add_user(cls, user: FisUser) -> bool:
        '''Añade un usuario a la base de datos. Si el usuario se ha añadido devuelve True,
        en caso contrario (si ya existe uno con el mismo id) devuelve `False`.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                c.execute('INSERT INTO Users VALUES (?,?,?,?,?)', 
                    (user.id, user.name, user.karma, user.level, user.xp))
            return True
        except sqlite3.IntegrityError:
            return False
    
    @classmethod
    def update_user(cls, user: FisUser) -> bool:
        '''Actualiza los datos de un usuario si existe en la base de datos. Si el usuario
        existe y se ha podido modificar devuelve `True`, en caso contrario devuelve `False`.'''

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

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
        except sqlite3.Error:
            return None
        if not result:
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
    def last_message_cooldown(cls, user_id)-> bool:
        '''Comprueba si la llamada a esta funcion y con la ultima llamada a la misma del mismo `user_id` es mayor que el cooldown'''

        now_time = time.time()
        try:
            with cls._connect() as conn:
                c = conn.cursor()
                last_time = c.execute('SELECT last_message FROM Messages WHERE id = ?', (user_id,)).fetchone()
        except sqlite3.Error:
            return False

        if not last_time:
            c.execute('INSERT INTO Messages (id,last_message) VALUES (?,?)', 
                (user_id, now_time))
            return True
        else:
            c.execute('UPDATE Messages SET last_message = ? WHERE id = ?', 
                (now_time, user_id))
            if now_time - last_time >= 30:
                return True
            else:
                return False