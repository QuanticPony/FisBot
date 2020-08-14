import discord
import random

class FisUser():
    def __init__(self, user):
        self.id = user.id
        self.name = user.nick
        self.karma = 0
        self.level = 0
        self.xp = 0
        return

    def addkarma(self):
        self.karma += 1
        return
    
    def xp_to_lvl_up(self) -> int:
        return self.xp * 10

    def addlevel(self):
        self.level += 1
        return

    def setlevel(self, lvl):
        self.level = lvl
        return
    
    def setkarma(self, krm):
        self.karma = krm
        return
    
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




