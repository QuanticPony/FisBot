import sqlite3
from sqlite3 import Connection
from ..classes.bot_class import BOT_PATH

class database():

    FILE_NAME = 'database.db'
    PATH = BOT_PATH

    SQL_TABLE: str # Debe contener la sentencia SQL que crea la tabla

    @classmethod
    def _create_db(cls) -> Connection:
        '''Crea la base de datos de FisBot'''

        with sqlite3.connect(cls.PATH + cls.FILE_NAME) as conn:
            c = conn.cursor()
            c.execute(cls.SQL_TABLE)
            return conn       

    @classmethod
    def _connect(cls) -> Connection:
        '''Intenta conectarse a la base de datos de nombre `FILE_NAME` y si esta no existe
        la crea. Devuelve una conexión a la base de datos.'''

        try:
            conn = sqlite3.connect('file:{}?mode=rw'.format(cls.PATH + cls.FILE_NAME), uri=True)
            conn.cursor().execute(cls.SQL_TABLE)
            return conn

        except sqlite3.OperationalError:
            return cls._create_db()