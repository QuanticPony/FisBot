import sqlite3
from sqlite3 import Connection

class database():

    FILE_NAME = 'database.db'

    SQL_TABLE: str # Debe contener la sentencia SQL que crea la tabla

    @classmethod
    def _create_db(cls) -> Connection:
        '''Crea la base de datos de FisBot'''
        
        with sqlite3.connect(cls.FILE_NAME) as conn:
            c = conn.cursor()
            c.execute(cls.SQL_TABLE)
            return conn       

    @classmethod
    def _connect(cls) -> Connection:
        '''Intenta conectarse a la base de datos de nombre `FILE_NAME` y si esta no existe
        la crea. Devuelve una conexión a la base de datos.'''

        try:
            return sqlite3.connect('file:{}?mode=rw'.format(cls.FILE_NAME), uri=True)

        except sqlite3.OperationalError:
            return cls._create_db()

    @classmethod
    def execute(cls, sentence, parameters) -> str:
        '''Ejecuta en la base de datos una sentencia SQL'''

        try: 
            conn = cls._connect()
            result = conn.cursor().execute(sentence, parameters)
            

        except sqlite3.OperationalError:
            conn = cls._create_db()
            result = conn.cursor().execute(sentence, parameters)

        except sqlite3.IntegrityError:
            return False

        except sqlite3.Error:
            return False

        if not result:
            return True
        return result