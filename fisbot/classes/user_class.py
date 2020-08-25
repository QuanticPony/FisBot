import random

class FisUser():
    def __init__(self, user_id, name, karma=0, level=0, xp=0):
        self.id = user_id
        self.name = name
        self.karma = karma
        self.level = level
        self.xp = xp

    def xp_to_lvl_up(self) -> int:
        return 300 + self.level * 10 
    
    def addxp(self) -> int:
        '''Sube la experiencia del usuario. Devuelve el nivel si se sube de nivel'''
        
        if self.level != 0:
            amount = random.randint(1, self.level) 
        else:
            amount = 10

        newxp = self.xp + amount
        xp_required = self.xp_to_lvl_up()
        if newxp >= xp_required:
            self.xp = newxp - xp_required
            self.level += 1
            return self.level
        else:
            self.xp = newxp
            return None





