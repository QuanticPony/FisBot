import random

class FisUser():
    def __init__(self, user_id, name, karma=0, level=0, xp=0):
        self.id = user_id
        self.name = name
        self.karma = karma
        self.level = level
        self.xp = xp

    def xp_to_lvl_up(self) -> int:
        return self.level * 10
    
    def addxp(self):
        
        if self.level != 0:
            amount = random.randint(1, self.level) 
        else:
            amount = 10

        newxp = self.xp + amount
        xp_required = xp_to_lvl_up(self)
        if newxp >= xp_required:
            self.xp = newxp - xp_required
            self.level += 1
        else:
            self.xp = newxp





