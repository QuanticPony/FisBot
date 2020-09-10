class Poll():
    CODE_POINT = 127462

    def __init__(self, title='Titulo', description='Descripcion', values=['Elemento 1']):
        self.index = 0
        self.options = {
            '🟫': ['Titulo', title],
            '🟩': ['Descripcion', description]
        }
        self.mention = 'Encuesta'
        self.options.update({f"{chr(self.index + self.CODE_POINT)}": [v, 'Null'] for self.index, v in enumerate(values)})

    def _mod_title(self) -> str:
        '''Devuelve el titulo utilizado en la modificacion de esta clase'''

        return 'Nueva encuesta:'
    
    def _mod_desc(self) -> str:
        '''Devuelve la descripcion utilizada en la modificacion de esta clase'''

        return '''❎ Añade una opcion y ❌ borra el campo con el emoticono que envies en tu siguiente mensaje. 
        Selecciona el campo a modificar:'''


    def add_element(self, value):
        '''Añade un nuevo elemento al objeto Poll'''

        self.index += 1
        element = [f'Elemento {self.index}', value]
        self.options[chr(self.index + self.CODE_POINT)] = element
        


    def mod_element(self, key, value):
        '''Modifica un elemento del objeto Poll'''

        self.options[key][1] = value


    def del_element(self, key) -> bool:
        '''Borra un campo del objeto Poll y devuelve `True`. Si ese campo es el titulo o la descripcion, devuelve `False`'''

        if key == '🟫' or '🟩':
            return False
        else:
            self.options.pop(key)
            self.index -= 1
            return True
    
    def return_values(self) -> dict:
        '''Devuelve los elementos de la encuesta en un diccionario cuya key es un `Emoji` y el value es la opcion'''

        dict_copy = self.options.copy()
        dict_copy.pop('🟫')
        dict_copy.pop('🟩')
        return dict_copy