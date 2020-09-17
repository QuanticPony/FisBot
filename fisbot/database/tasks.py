from ..classes.task_class import FisTask
from .base import database
import sqlite3
from sqlite3 import Connection

class ProyectsDB(database):

    SQL_TABLE ='''CREATE TABLE IF NOT EXISTS Tasks (
        id INTEGER PRIMARY KEY,
        subject text,
        title text,
        description text,
        day integer,
        month text,
        year integer,
        school_year integer,
        url text
        )'''

    @classmethod
    def add_task(cls, task: FisTask) -> bool:
        '''Añade una tarea a la base de datos. Si la tarea se ha añadido devuelve True,
        en caso contrario (si ya existe uno con el mismo id) devuelve `False`.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                c.execute('INSERT INTO Tasks (subject, title, description, day, month, year, school_year, url) VALUES (?,?,?,?,?,?,?,?)', 
                    (task.subject, task.title, task.description, task.day, task.month, task.year, task.school_year, task.url))
            return True
        except sqlite3.IntegrityError:
            return False

    @classmethod
    def update_task(cls, task: FisTask) -> bool:
        '''Actualiza los datos de una tarea si existe en la base de datos. Si la tarea
        existe y se ha podido modificar devuelve `True`, en caso contrario devuelve `False`.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                c.execute('UPDATE Tasks SET subject = ?, title = ?, description = ?, day = ?, month=?, year = ?, school_year = ?, url = ? WHERE id = ?', 
                    (task.subject, task.title, task.description, task.day, task.month, task.year, task.school_year, task.url, task.id))
            return True
        except sqlite3.Error:
            return False

    @classmethod
    def del_task(cls, task) -> bool:
        '''Elimina una tarea de la base de datos si su id coincide con el de `task`. 
        Si no se introduce `task` asume que has llamado a esta funcion desde un objeto `FisTask` y lo borra.
        Si la tarea se ha eliminado devuelve `True`, en caso contrario devuelve `False`.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                c.execute('DELETE FROM Tasks WHERE id = ?', (task.id,))
            return True
        except sqlite3.Error:
            return False

    @classmethod
    def get_task(cls, task_id) -> FisTask:
        '''Obtiene una tarea de la base de datos si su id coincide con `task_id`.
        Si la tarea no se encuentra devuelve `None`.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Tasks WHERE id = ?', (task_id,)).fetchone()
        except sqlite3.Error:
            return None
        if not result:
            return None
        return FisTask(*result)

    @classmethod
    def get_all_tasks(cls) -> tuple:
        '''Devuelve una colección de todas las tareas registrados en la base de datos
        ordenadas por asignaturas.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Tasks ORDER BY subject').fetchall()
        except sqlite3.Error:
            return None
        return tuple([FisTask(*user) for user in result])

    @classmethod
    def get_all_subject_tasks(cls, subject) -> tuple:
        '''Devuelve una colección de todas las tareas registrados en la base de datos
        con la asignatura especificada.'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT * FROM Tasks WHERE subject = ? ORDER BY title',\
                 (subject,)).fetchall()
        except sqlite3.Error:
            return None
        return tuple([FisTask(*user) for user in result])

    @classmethod
    def subjects(cls) -> list:
        '''Devuelve una coleccion de los nombres de todas las asignaturas'''

        try:
            with cls._connect() as conn:
                c = conn.cursor()
                result = c.execute('SELECT DISTINCT subject FROM Tasks').fetchall()
            
        except sqlite3.Error:
            return None
        return list(element[0] for element in result)

    @classmethod
    def get_all_school_year_subjects(cls) -> tuple:...
    @classmethod
    def get_all_school_year_tasks(cls) -> tuple:...