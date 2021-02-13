import sqlite3
import time
from sqlite3 import Connection

from .base import database


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
    def add_user(cls, user) -> bool:
        '''Añade un usuario a la base de datos. Si el usuario se ha añadido devuelve True,
        en caso contrario (si ya existe uno con el mismo id) devuelve `False`.'''

        confirmation = cls.execute('INSERT INTO Users VALUES (?,?,?,?,?,?,?)', args=(user.id, user.name, user.karma, user.level, user.xp, user.last_message, user.last_join))
        if confirmation:
            return True
        return cls.update_user(user)
    
    @classmethod
    def update_user(cls, user) -> bool:
        '''Actualiza los datos de un usuario si existe en la base de datos. Si el usuario
        existe y se ha podido modificar devuelve `True`, en caso contrario devuelve `False`.'''

        return cls.execute('UPDATE Users SET name = ?, karma = ?, level = ?, xp = ? WHERE id = ?', args=(user.name, user.karma, user.level, user.xp, user.id))
    
    @classmethod
    def del_user(cls, user) -> bool:
        '''Elimina un usuario de la base de datos si su id coincide con el de `user`. 
        Si el usuario se ha eliminado devuelve `True`, en caso contrario devuelve `False`.'''

        return cls.execute('DELETE FROM Users WHERE id = ?', args=(user.id,))
    
    @classmethod
    def get_user(cls, user_id) -> list:
        '''Obtiene un usuario de la base de datos si su id coincide con `user_id`.
        Si el usuario no se encuentra devuelve `None`.'''

        if not user_id:
            return False
        result = cls.execute('SELECT * FROM Users WHERE id = ?', args=(user_id,)).fetchone()

        #if not result:
        #    cls.execute('INSERT INTO Users (id) VALUES (?)', args=(user_id,))
        #    return None
        return result
    
    @classmethod
    def get_all_users(cls) -> tuple:
        '''Devuelve una colección de todos los usuarios registrados en la base de datos
        ordenados alfabéticamente.'''

        result = cls.execute('SELECT * FROM Users ORDER BY name').fetchall()
        return result


    @classmethod
    def new_voice_join(cls, user_id):
        '''Permite ingresar el momento en el que el usuario de id especificada se conecto a un canal de voz por ultima vez.
        Devuelve `True` si lo ha conseguido actualizar en la base de datos'''

        now_time = time.time()
        if not user_id:
            return False
        
        return cls.execute('UPDATE Users SET last_join = ? WHERE id = ?', args=(now_time, user_id))

    @classmethod
    def last_voice_join(cls, user_id)-> (bool, list):
        '''Devuelve la hora en la que se conecto el usuario por ultima vez.
        Devuelve el usuario de la base de datos con mismo id'''

        now_time = time.time()
        if user_id:
            last_time , = cls.execute('SELECT last_join FROM Users WHERE id = ?', args=(user_id,)).fetchone()
            user = cls.get_user(user_id)
            if user:
                cls.execute('UPDATE Users SET last_join = ? WHERE id = ?', args=(now_time, user_id))
                return (now_time - last_time, user)
        return (False, None)