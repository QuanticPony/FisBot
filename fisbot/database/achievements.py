import sqlite3
import time
from sqlite3 import Connection

from .base import database


class AchievementsDB(database):

    SQL_TABLE ='''CREATE TABLE IF NOT EXISTS "Achievements" (
	"id"	INTEGER NOT NULL,
	"color"	TEXT,
	"extras"	TEXT,
	"C1_de_2020_2021"	INTEGER,
	"C2_de_2020_2021"	INTEGER,
	"C1_de_2021_2022"	INTEGER,
	"C2_de_2021_2022"	INTEGER,
	"C1_de_2022_2023"	INTEGER,
	"C2_de_2022_2023"	INTEGER,
	PRIMARY KEY("id"))'''
    
    @classmethod
    def add_achievement(cls, achiev) -> bool:
        '''Añade un usuario a la base de datos. Si el usuario se ha añadido devuelve True,
        en caso contrario (si ya existe uno con el mismo id) devuelve `False`.'''

        tup = tuple(i[1] for i in achiev.level_s_y)
        confirmation = cls.execute('INSERT INTO Achievements VALUES (?,?,?,'+ ','.join(['?' for i in achiev.level_s_y]) + ')', 
            args=(achiev.id, ' '.join(achiev.color),achiev.extras, *tup))
        if confirmation:
            return True
        return cls.update_achiev(achiev)
    
    @classmethod
    def update_achievement(cls, achiev) -> bool:
        '''Actualiza los datos de un usuario si existe en la base de datos. Si el usuario
        existe y se ha podido modificar devuelve `True`, en caso contrario devuelve `False`.'''

        tup = tuple(i[1] for i in achiev.level_s_y if i)
        tup_names = tuple(f'"{i[0]}"=?' for i in achiev.level_s_y if i)

        return cls.execute('UPDATE Achievements SET color=?, extras=?,' + ', '.join(tup_names) +' WHERE id = ?',
            args=( ' '.join(map(str, achiev.color)),achiev.extras, *tup, achiev.id))
    
    @classmethod
    def del_achievement(cls, achiev) -> bool:
        '''Elimina un usuario de la base de datos si su id coincide con el de `achiev`. 
        Si el usuario se ha eliminado devuelve `True`, en caso contrario devuelve `False`.'''

        return cls.execute('DELETE FROM Achievements WHERE id = ?', args=(achiev.id,))
    
    @classmethod
    def get_achievements(cls, achiev_id) -> list:
        '''Obtiene un usuario de la base de datos si su id coincide con `achiev_id`.
        Si el usuario no se encuentra devuelve `None`.'''

        if not achiev_id:
            return None
        result = cls.execute('SELECT * FROM Achievements WHERE id = ?', args=(achiev_id,)).fetchone()

        if not result:
            cls.execute('INSERT INTO Achievements (id, color) VALUES (?,?)', args=(achiev_id, '50 50 150'))
            return None
        return result

    @classmethod
    def insert_all(cls, id_list):

        for i in id_list:
             cls.execute('INSERT INTO Achievements (id, color) VALUES (?,?)', args=(i, '50 50 150'))