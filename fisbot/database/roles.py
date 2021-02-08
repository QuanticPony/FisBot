import sqlite3
from sqlite3 import Connection

from .base import database


class RolesDB(database):

    SQL_TABLE = '''CREATE Table IF NOT EXISTS Roles (
        rol_id integer NOT NULL PRIMARY KEY,
        lvl integer,
        description text,
        privileges text,
        guild_id integer
        )'''

    @classmethod
    def add_rol(cls, rol) -> bool:
        '''Añade un rol a la base de datos. Si el rol se ha añadido devuelve True,
        en caso contrario (si ya existe uno con el mismo id) devuelve `False`.'''

        cls.execute('INSERT INTO Roles VALUES (?,?,?,?,?)', args=(rol.id, rol.level, rol.description, rol.privileges, rol.guild_id))
  

    @classmethod
    def update_rol(cls, rol) -> bool:
        '''Actualiza los datos de un rol si existe en la base de datos. Si el rol
        existe y se ha podido modificar devuelve `True`, en caso contrario devuelve `False`.'''

        cls.execute('UPDATE Roles SET lvl = ?, description = ?, privileges = ? WHERE rol_id = ?', args=(rol.level, rol.description, rol.privileges, rol.id))

    @classmethod
    def del_rol(cls, rol) -> bool:
        '''Elimina un rol de la base de datos si su id coincide con el de `rol`. 
        Si el rol se ha eliminado devuelve `True`, en caso contrario devuelve `False`.'''

        cls.execute('DELETE FROM Roles WHERE rol_id = ?', args=(rol.id,))


    @classmethod
    def get_roles(cls, level, *, guild_id=None) -> list:
        '''Devuelve todos los roles que tengan el mismo `level`.
        Si se introduce la id del servidor `guild_id` un rol de la base de datos si su nivel coincide con `level`.
        Si el rol no se encuentra devuelve `None`.'''

        if guild_id:
            result = cls.execute('SELECT * FROM Roles WHERE lvl = ? AND guild_id = ?', args=(level, guild_id)).fetchone()
        else:
            result = cls.execute('SELECT * FROM Roles WHERE lvl = ?', args=(level,)).fetchall()

        if not result:
            return None
        return result

    @classmethod
    def get_rol_id(cls, rol_id) -> list:
        '''Obtiene un rol de la base de datos si su id coincide con `rol_id`.
        Si el rol no se encuentra devuelve `None`.'''

        result = cls.execute('SELECT * FROM Roles WHERE rol_id = ?', args=(rol_id,)).fetchone()
        
        if not result:
            return None
        return result

    @classmethod
    def get_all_guild_roles(cls, guild_id) -> list:
        '''Devuelve una colección de todos los roles registrados en la base de datos
        ordenados por nivel necesario.'''

        result = cls.execute('SELECT * FROM Roles WHERE guild_id = ? ORDER BY lvl ', args=(guild_id,)).fetchall()
        return result

    @classmethod
    def get_all_roles(cls) -> list:
        '''Devuelve una colección de todos los roles registrados en la base de datos
        ordenados por nivel necesario.'''

        result = cls.execute('SELECT * FROM Roles ORDER BY lvl ').fetchall()
        return result
