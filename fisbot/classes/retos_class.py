import random
import discord 

class FisReto():
    
    def __init__(self, user_id=0, type = '', title = '', description= '', day=0, month=0, year=0, prize='' ):
        self.id = user_id
        self.type = type
        self.title = title
        self.description = description
        self.day = day
        self.month = month
        self.year = year
        self.prize = prize
        from ..database.retos import retosDB
        self.database = retosDB

#TODO: funciones que afecten a esta clase, si no me equiboco