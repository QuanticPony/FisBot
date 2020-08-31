from ..classes.user_class import FisUser
import sqlite3
from sqlite3 import Connection
import time
from .. import BOT_PATH

class UsersDB():

    FILE_NAME = 'database.db'

    def _create_db(self) -> Connection:
        '''Crea una base de datos para usuarios FisBot y devuelve una conexión a esta.
        El nombre del archivo en disco se especifica con el atributo de clase `FILE_NAME`'''

        with sqlite3.connect(BOT_PATH + self.FILE_NAME) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE Users (
                            id text NOT NULL PRIMARY KEY,
                            name text,
                            karma integer,
                            level integer,
                            xp integer
                        )''')
            return conn

    def _connect(self) -> Connection:
        '''Intenta conectarse a la base de datos de nombre `FILE_NAME` y si esta no existe
        la crea. Devuelve una conexión a la base de datos.'''

        try:
            return sqlite3.connect('file:{}?mode=rw'.format(BOT_PATH + self.FILE_NAME), uri=True)
        except sqlite3.OperationalError:
            return self._create_db()

    def add_user(self, user: FisUser) -> bool:
        '''Añade un usuario a la base de datos. Si el usuario se ha añadido devuelve True,
        en caso contrario (si ya existe uno con el mismo id) devuelve `False`.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('INSERT INTO Users VALUES (?,?,?,?,?)', 
                    (user.id, user.name, user.karma, user.level, user.xp))
            return True
        except sqlite3.IntegrityError:
            return False

    def update_user(self, user: FisUser) -> bool:
        '''Actualiza los datos de un usuario si existe en la base de datos. Si el usuario
        existe y se ha podido modificar devuelve `True`, en caso contrario devuelve `False`.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('UPDATE Users SET name = ?, karma = ?, level = ?, xp = ? WHERE id = ?', 
                    (user.name, user.karma, user.level, user.xp, user.id))
            return True
        except sqlite3.Error:
            return False

    def del_user(self, user: FisUser) -> bool:
        '''Elimina un usuario de la base de datos si su id coincide con el de `user`. 
        Si el usuario se ha eliminado devuelve `True`, en caso contrario devuelve `False`.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('DELETE FROM Users WHERE id = ?', (user.id,))
            return True
        except sqlite3.Error:
            return False

    def get_user(self, user_id) -> FisUser:
        '''Obtiene un usuario de la base de datos si su id coincide con `user_id`.
        Si el usuario no se encuentra devuelve `None`.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
        except sqlite3.Error:
            return None
        if not result:
            return None
        return FisUser(*result)

    def get_all_users(self) -> tuple:
        '''Devuelve una colección de todos los usuarios registrados en la base de datos
        ordenados alfabéticamente.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Users ORDER BY name').fetchall()
        except sqlite3.Error:
            return None
        return tuple([FisUser(*user) for user in result])


    def last_message_cooldown(self, user_id)-> bool:
        '''Comprueba si la llamada a esta funcion y con la ultima llamada a la misma del mismo `user_id` es mayor que el cooldown'''

        now_time = time.time()
        try:
            with self._connect() as conn:
                c = conn.cursor()
                last_time = c.execute('SELECT last_message FROM Messages WHERE id = ?', (user_id,)).fetchone()
        except sqlite3.Error:
            return False

        if not last_time:
            c.execute('INSERT INTO Messages VALUES (?,?)', 
                (user_id, now_time))
            return True
        else:
            c.execute('UPDATE Messages SET last_message = ? WHERE id = ?', 
                (now_time, user_id))
            if now_time - last_time >= 5:
                return True
            else:
                return False