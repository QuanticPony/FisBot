from ..classes.rol_class import FisRol
import sqlite3
from sqlite3 import Connection

class RolesDB():

    FILE_NAME = 'database.db'

    def _create_db(self) -> Connection:
        '''Crea una base de datos para roles FisRol y devuelve una conexión a esta.
        El nombre del archivo en disco se especifica con el atributo de clase `FILE_NAME`'''

        with sqlite3.connect(self.FILE_NAME) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE Roles (
                            rol_id integer NOT NULL PRIMARY KEY,
                            lvl integer,
                            description text,
                            privileges text
                        )''')
            return conn

    def _connect(self) -> Connection:
        '''Intenta conectarse a la base de datos de nombre `FILE_NAME` y si esta no existe
        la crea. Devuelve una conexión a la base de datos.'''

        try:
            return sqlite3.connect('file:{}?mode=rw'.format(self.FILE_NAME), uri=True)
        except sqlite3.OperationalError:
            return self._create_db()

    def add_rol(self, rol: FisRol) -> bool:
        '''Añade un rol a la base de datos. Si el rol se ha añadido devuelve True,
        en caso contrario (si ya existe uno con el mismo id) devuelve `False`.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('INSERT INTO Roles VALUES (?,?,?,?)', 
                    (rol.rol_id, rol.level, rol.description, rol.privileges))
            return True
        except sqlite3.IntegrityError:
            return False

    def update_rol(self, rol: FisRol) -> bool:
        '''Actualiza los datos de un rol si existe en la base de datos. Si el rol
        existe y se ha podido modificar devuelve `True`, en caso contrario devuelve `False`.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('UPDATE Roles SET lvl = ?, description = ?, privileges = ? WHERE id = ?', 
                    (rol.level, rol.description, rol.privileges, rol.rol_id))
            return True
        except sqlite3.Error:
            return False

    def del_rol(self, rol: FisRol) -> bool:
        '''Elimina un rol de la base de datos si su id coincide con el de `rol`. 
        Si el rol se ha eliminado devuelve `True`, en caso contrario devuelve `False`.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('DELETE FROM Roles WHERE id = ?', (rol.rol_id,))
            return True
        except sqlite3.Error:
            return False

    def get_rol(self, level) -> FisRol:
        '''Obtiene un rol de la base de datos si su id coincide con `rol_id`.
        Si el rol no se encuentra devuelve `None`.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Roles WHERE lvl = ?', (level,)).fetchone()
        except sqlite3.Error:
            return None
        if not result:
            return None
        return FisRol(*result)

    def get_all_roles(self) ->list:
        '''Devuelve una colección de todos los roles registrados en la base de datos
        ordenados por nivel necesario.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Roles ORDER BY lvl').fetchall()
        except sqlite3.Error:
            return None
        return list([FisRol(*rol) for rol in result])

