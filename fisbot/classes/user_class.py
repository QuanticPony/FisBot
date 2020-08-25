import random
import discord

class FisUser():

    BASE_XP = 300
    XP_MULTIPLAYER = 10
    XP_ADD_BASE = 10
    XP_MAX_MULT = 5

    def __init__(self, user_id=0, name='', karma=0, level=0, xp=0):
        self.id = user_id
        self.name = name
        self.karma = karma
        self.level = level
        self.xp = xp
        from ..database.users import UsersDB
        self.database = UsersDB()


    def xp_to_lvl_up(self) -> int:
        return BASE_XP + self.level * XP_MULTIPLAYER 
    
    def addxp(self) -> int:
        '''Sube la experiencia del usuario. Devuelve el nivel si se sube de nivel'''
        
        if self.level != 0:
            amount = random.randint(XP_MAX_MULT) * self.level
        else:
            amount = XP_ADD_BASE

        newxp = self.xp + amount
        xp_required = self.xp_to_lvl_up()
        if newxp >= xp_required:
            self.xp = newxp - xp_required
            self.level += 1
            return self.level
        else:
            self.xp = newxp
            return None





