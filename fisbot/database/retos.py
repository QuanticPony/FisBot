from ..classes.reto_class import FisReto
import sqlite3
from sqlite3 import Connection

class ChallengesDB():

    FILE_NAME = 'database.db'

    def _create_db(self) -> Connection:
        '''Crea una base de datos para retos y devuelve una conexión a esta'''

        with sqlite3.connect(self.FILE_NAME) as conn:
            c= conn.cursor()
            c.execute('''CREATE TABLE Reto(
                            id INTERGER PRIMERY KEY,
                            type text,
                            title text,
                            description text,
                            day integer,
                            month integer,
                            year integer,
                            prize text
                        )'''
            )
            return conn

def _connect(self) -> Connection:
    '''Intenta conectarse a la base de datos de nombre  'FILE_NAME' y si esta no existe
    la crea. Devuelve una conexión a la base de datos.'''

    try:
        return sqlite3.connect('file:{}?mode=rw'.format(self.FILE_NAME), uri=True)
    except sqlite3.OperationalError:
        return self._create_db()

def add_reto(self, reto:FisReto) ->bool:
    '''Añade un reto a la base de datos. Si el reto se ha añadido devuelve true,
    en caso contrario (si ya existe uno con el mismo id) devuelve 'False'.'''

    try:
        with self._connect() as conn:
            c= conn.cursor()
            c.execute('INSERT INTO retos (type, title, description, day, month, year, prize) VALUES(?,?,?,?,?,?,?)',
                (reto.type, reto.title, reto.description, reto.day, reto.month, reto.year, reto.prize))
        return True
    except sqlite3.IntegrityError:
        return False

