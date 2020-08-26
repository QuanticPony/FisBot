from ..classes.task_class import FisTask
import sqlite3
from sqlite3 import Connection


class ProyectsDB():

    FILE_NAME = 'database.db'

    def _create_db(self) -> Connection:
        '''Crea una base de datos para trabajos y devuelve una conexión a esta.
        El nombre del archivo en disco se especifica con el atributo de clase `FILE_NAME`'''

        # TODO: mover creacion a otro archivo y unificar la creacion de las dos tablas
        with sqlite3.connect(self.FILE_NAME) as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE Tasks (
                            id INTEGER PRIMARY KEY,
                            subject text,
                            title text,
                            description text,
                            day integer,
                            month text,
                            year integer
                        )''')
            return conn

    def _connect(self) -> Connection:
        '''Intenta conectarse a la base de datos de nombre `FILE_NAME` y si esta no existe
        la crea. Devuelve una conexión a la base de datos.'''

        try:
            return sqlite3.connect('file:{}?mode=rw'.format(self.FILE_NAME), uri=True)
        except sqlite3.OperationalError:
            return self._create_db()

    def add_task(self, task: FisTask) -> bool:
        '''Añade una tarea a la base de datos. Si la tarea se ha añadido devuelve True,
        en caso contrario (si ya existe uno con el mismo id) devuelve `False`.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('INSERT INTO Tasks (subject, title, description, day, month, year) VALUES (?,?,?,?,?,?)', 
                    (task.subject, task.title, task.description, task.day, task.month, task.year))
            return True
        except sqlite3.IntegrityError:
            return False

    def update_task(self, task: FisTask) -> bool:
        '''Actualiza los datos de una tarea si existe en la base de datos. Si la tarea
        existe y se ha podido modificar devuelve `True`, en caso contrario devuelve `False`.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('UPDATE Tasks SET subject = ?, title = ?, description = ?, day = ?, month=?, year = ? WHERE id = ?', 
                    (task.subject, task.title, task.description, task.day, task.month, task.year, task._id))
            return True
        except sqlite3.Error:
            return False

    def del_task(self, task) -> bool:
        '''Elimina una tarea de la base de datos si su id coincide con el de `task`. 
        Si no se introduce `task` asume que has llamado a esta funcion desde un objeto `FisTask` y lo borra.
        Si la tarea se ha eliminado devuelve `True`, en caso contrario devuelve `False`.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                c.execute('DELETE FROM Tasks WHERE id = ?', (task._id,))
            return True
        except sqlite3.Error:
            return False

    def get_task(self, task_id) -> FisTask:
        '''Obtiene una tarea de la base de datos si su id coincide con `task_id`.
        Si la tarea no se encuentra devuelve `None`.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Tasks WHERE id = ?', (task_id,)).fetchone()
        except sqlite3.Error:
            return None
        if not result:
            return None
        return FisTask(*result)

    def get_all_tasks(self) -> tuple:
        '''Devuelve una colección de todas las tareas registrados en la base de datos
        ordenadas por asignaturas.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Tasks ORDER BY subject').fetchall()
        except sqlite3.Error:
            return None
        return tuple([FisTask(*user) for user in result])

    def get_all_subject_tasks(self, subject) -> tuple:
        '''Devuelve una colección de todas las tareas registrados en la base de datos
        con la asignatura especificada.'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Tasks WHERE subject = ? ORDER BY title',\
                 (subject,)).fetchall()
        except sqlite3.Error:
            return None
        return tuple([FisTask(*user) for user in result])

    def subjects(self) -> list:
        '''Devuelve una coleccion de los nombres de todas las asignaturas'''

        try:
            with self._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT DISTINCT subject FROM Tasks').fetchall()
            
        except sqlite3.Error:
            return None
        return list(element[0] for element in result)