from ..database import achievements

class Achievements():
    
    def __init__(self, user_id, color='50 50 150', extras='', *level_s_y):
        self.id	= user_id
        self.color = tuple(map(int, color.split()))
        self.extras = extras
        if not level_s_y:
            self.level_s_y = []
        self.level_s_y = list([self._to_str(i), level] for i, level in enumerate(level_s_y))


    @classmethod
    def _to_index(cls, s, y):
        return int((y - 2020)*2 + s - 1)

    @classmethod
    def _to_str(cls, i):
        s, y = 1 + i%2 , 2020 + int((i - i%2)/2)
        return f"C{s}_de_{y}_{y+1}"

    def _color_to_str(self):
        return f"{self.color[0]} {self.color[1]} {self.color[2]}"
        
    @classmethod
    def convert_from_database(cls, funcion, *, args=[]):
        '''Ejecuta la funcion `funcion` con los argumentos dados en la base de datos. Convierte el resultado a un
        objeto Achievements'''

        if args:
            _return = funcion(args)
        else: 
            _return = funcion()

        try:
            result = cls(*_return)
        except:
            return None
        return result

    @classmethod
    def add_achievement(cls, user, semester, year):

        ach = cls.get_achievement(user)
        if not ach:
            ach = cls(user_id=user.id)
        
        index = cls._to_index(int(semester), int(year))

        if len(ach.level_s_y) <= index:
            for i in range(index):
                ach.level_s_y.append([cls._to_str(i), 0])

            ach.level_s_y.append([cls._to_str(index), user.level])
        else:
            ach.level_s_y.insert(index, [cls._to_str(index), user.level])
        ach.update()


    @classmethod
    def get_achievement(cls, user):

        ach = cls.convert_from_database(achievements.AchievementsDB.get_achievements, args=user.id)
        if not ach:
            ach = cls(user.id)
            achievements.AchievementsDB.add_achievement(ach)
        return ach

    def update(self):
        '''Actualiza los logros en la base de datos'''
        try:
            achievements.AchievementsDB.update_achievement(self)
        except:
            achievements.AchievementsDB.add_achievement(self)

    def set_color(self, r, g, b):
        '''Cambia el color y actualiza la base de datos'''

        self.color = (r, g, b)
        self.update()