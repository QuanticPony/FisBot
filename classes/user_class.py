import random

class FisUser():
    def __init__(self, user_id, name, karma=0, level=0, xp=0):
        self.id = user_id
        self.name = name
        self.karma = karma
        self.level = level
        self.xp = xp

    def addkarma(self):
        self.karma += 1
    
    def xp_to_lvl_up(self) -> int:
        return self.xp * 10

    def addlevel(self):
        self.level += 1

    def setlevel(self, lvl):
        self.level = lvl
    
    def setkarma(self, krm):
        self.karma = krm
    
    def addxp(self, amount):
        newxp = self.xp + amount
        xp_required = xp_to_lvl_up(self)
        if newxp >= xp_required:
            addlevel(self)
            self.xp = newxp - xp_required
        else:
            self.xp = newxp

    def setxp(self, exp):
        self.xp += exp

    def read_user(self, ):
        self.level = int
        self.xp = int
        self.karma = int


    def modifi_user(self, ):
        pass

    def write_user(self, ):
        pass




