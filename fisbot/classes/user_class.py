import random
import discord
from .display_class import Display

class FisUser(Display):

    BASE_XP = 300
    XP_MULTIPLAYER = 10
    XP_ADD_BASE = 10
    XP_MAX_MULT = 5

    def __init__(self, user_id=0, name='', karma=0, level=0, xp=0):
        self.id = int(user_id)
        self.name = name
        self.karma = int(karma)
        self.level = int(level)
        self.xp = int(xp)
        from ..database.users import UsersDB
        self.database = UsersDB()

    @classmethod
    def init_with_member(cls, member: discord.Member):
        '''Devuelve un usuario `FisUser` a partir de un miembro'''

        return cls().database.get_user(member.id)

    def _mod_title(self) -> str:
        '''Devuelve el titulo utilizado en la modificacion de esta clase'''

        return f"Modificar usuario id={self.id}"
    
    def _mod_desc(self) -> str:
        '''Devuelve la descripcion utilizada en la modificacion de esta clase'''

        return '''Abajo tienes la lista de todos los campos modificables. 
    Si quieres modificar uno mas de una vez desseleccionalo y vuelvelo a seleccionar.
    *Cuando hayas acabado* presiona el boton de guardar'''


    async def modify(self, ctx) -> bool:
        return await modify(self, ctx, user=True)

    def xp_to_lvl_up(self) -> int:
        return self.BASE_XP + self.level * self.XP_MULTIPLAYER 
    
    def addxp(self) -> int:
        '''Sube la experiencia del usuario. Devuelve el nivel si se sube de nivel'''
        
        if self.level != 0:
            amount = self.XP_ADD_BASE + random.randint(1, self.level)
        else:
            amount = self.XP_ADD_BASE

        newxp = self.xp + amount
        xp_required = self.xp_to_lvl_up()
        if newxp >= xp_required:
            self.xp = newxp - xp_required
            self.level += 1
            return self.level
        else:
            self.xp = newxp
            return None