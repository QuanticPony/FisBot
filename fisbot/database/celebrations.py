import sqlite3
from sqlite3 import Connection

from .base import database


class CelebrationDB(database):

    SQL_TABLE = '''CREATE TABLE IF NOT EXIST Celebrations (
        celebration_id integer NOT NULL PRIMARY KEY,
        description text,
        )'''

    @classmethod
    def add_celebration(cls, celebration) -> bool:
        '''Añade un celebration a la base de datos. Si el celebration se ha añadido devuelve True,
        en caso contrario (si ya existe uno con el mismo id) devuelve `False`.'''

        cls.execute('INSERT INTO Celebrations VALUES (?,?,?,?,?)', args=(celebration.id, celebration.level, celebration.description, celebration.privileges, celebration.guild_id))
  

    @classmethod
    def update_celebration(cls, celebration) -> bool:
        '''Actualiza los datos de un celebration si existe en la base de datos. Si el celebration
        existe y se ha podido modificar devuelve `True`, en caso contrario devuelve `False`.'''

        cls.execute('UPDATE Celebrations SET lvl = ?, description = ?, privileges = ? WHERE celebration_id = ?', args=(celebration.level, celebration.description, celebration.privileges, celebration.id))

    @classmethod
    def del_celebration(cls, celebration) -> bool:
        '''Elimina un celebration de la base de datos si su id coincide con el de `celebration`. 
        Si el celebration se ha eliminado devuelve `True`, en caso contrario devuelve `False`.'''

        cls.execute('DELETE FROM Celebrations WHERE celebration_id = ?', args=(celebration.id,))


    @classmethod
    def get_celebrationes(cls, level, *, guild_id=None) -> list:
        '''Devuelve todos los celebrationes que tengan el mismo `level`.
        Si se introduce la id del servidor `guild_id` un celebration de la base de datos si su nivel coincide con `level`.
        Si el celebration no se encuentra devuelve `None`.'''

        if guild_id:
            result = cls.execute('SELECT * FROM Celebrations WHERE lvl = ? AND guild_id = ?', args=(level, guild_id)).fetchone()
        else:
            result = cls.execute('SELECT * FROM Celebrations WHERE lvl = ?', args=(level,)).fetchall()

        if not result:
            return None
        return result

    @classmethod
    def get_celebration_id(cls, celebration_id) -> list:
        '''Obtiene un celebration de la base de datos si su id coincide con `celebration_id`.
        Si el celebration no se encuentra devuelve `None`.'''

        result = cls.execute('SELECT * FROM Celebrations WHERE celebration_id = ?', args=(celebration_id,)).fetchone()
        
        if not result:
            return None
        return result

    @classmethod
    def get_all_guild_celebrationes(cls, guild_id) -> list:
        '''Devuelve una colección de todos los celebrationes registrados en la base de datos
        ordenados por nivel necesario.'''

        result = cls.execute('SELECT * FROM Celebrations WHERE guild_id = ? ORDER BY lvl ', args=(guild_id,)).fetchall()
        return result

    @classmethod
    def get_all_celebrationes(cls) -> list:
        '''Devuelve una colección de todos los celebrationes registrados en la base de datos
        ordenados por nivel necesario.'''

        result = cls.execute('SELECT * FROM Celebrations ORDER BY lvl ').fetchall()
        return result
