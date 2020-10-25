from ..classes.rol_class import FisRol
from .base import database
import sqlite3
from sqlite3 import Connection

class RolesDB(database):

    SQL_TABLE = '''CREATE Table IF NOT EXISTS Roles (
        rol_id integer NOT NULL PRIMARY KEY,
        lvl integer,
        description text,
        privileges text,
        guild_id integer
        )'''

    @classmethod
    def add_rol(cls, rol: FisRol) -> bool:
        '''Añade un rol a la base de datos. Si el rol se ha añadido devuelve True,
        en caso contrario (si ya existe uno con el mismo id) devuelve `False`.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                c.execute('INSERT INTO Roles VALUES (?,?,?,?,?)', 
                    (rol.id, rol.level, rol.description, rol.privileges, rol.guild_id))
            return True
        except sqlite3.IntegrityError:
            return False

    @classmethod
    def update_rol(cls, rol: FisRol) -> bool:
        '''Actualiza los datos de un rol si existe en la base de datos. Si el rol
        existe y se ha podido modificar devuelve `True`, en caso contrario devuelve `False`.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                c.execute('UPDATE Roles SET lvl = ?, description = ?, privileges = ? WHERE rol_id = ?', 
                    (rol.level, rol.description, rol.privileges, rol.id))
            return True
        except sqlite3.Error:
            return False

    @classmethod
    def del_rol(cls, rol: FisRol) -> bool:
        '''Elimina un rol de la base de datos si su id coincide con el de `rol`. 
        Si el rol se ha eliminado devuelve `True`, en caso contrario devuelve `False`.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                c.execute('DELETE FROM Roles WHERE rol_id = ?', (rol.id,))
            return True
        except sqlite3.Error:
            return False

    @classmethod
    def get_roles(cls, level, *, guild_id=None) -> list:
        '''Devuelve todos los roles que tengan el mismo `level`.
        Si se introduce la id del servidor `guild_id` un rol de la base de datos si su nivel coincide con `level`.
        Si el rol no se encuentra devuelve `None`.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                if guild_id:
                    result = c.execute('SELECT * FROM Roles WHERE lvl = ? AND guild_id = ?', (level, guild_id)).fetchone()
                else:
                    result = c.execute('SELECT * FROM Roles WHERE lvl = ?', (level,)).fetchall()
        except sqlite3.Error:
            return None
        if not result:
            return None
        return list([FisRol(*rol) for rol in result])

    @classmethod
    def get_rol_id(cls, rol_id) -> FisRol:
        '''Obtiene un rol de la base de datos si su id coincide con `rol_id`.
        Si el rol no se encuentra devuelve `None`.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Roles WHERE rol_id = ?', (rol_id,)).fetchone()
        except sqlite3.Error:
            return None
        if not result:
            return None
        return FisRol(*result)

    @classmethod
    def get_all_guild_roles(cls, guild_id) -> list:
        '''Devuelve una colección de todos los roles registrados en la base de datos
        ordenados por nivel necesario.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Roles WHERE guild_id = ? ORDER BY lvl ', (guild_id,)).fetchall()
        except sqlite3.Error:
            return None
        return list([FisRol(*rol) for rol in result])

    @classmethod
    def get_all_roles(cls) -> list:
        '''Devuelve una colección de todos los roles registrados en la base de datos
        ordenados por nivel necesario.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Roles ORDER BY lvl ').fetchall()
        except sqlite3.Error:
            return None
        return list([FisRol(*rol) for rol in result])