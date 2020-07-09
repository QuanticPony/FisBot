import discord
import random

class User(commands.Context):
    '''Usuario o miembro del servidor de UNIZAR'''

    async def __init__(self, user_id, file, dictionary):
        self.name = name
        self.karma = 0
        self.level = 0
        self.xp = 0
        dictionary.setdefault(user_id, sum(1 for line in file))
        file.seek(0,2)
        file.write(str(self))
       
    
    async def display(self, message):
        embed = discord.Embed(title="{self.name}", description="Estas son tus estadísticas:\n'''css", color=0x18F309)
        embed.add_field(name="Level", value="Nivel:{self.level}")
        embed.add_field(name="xp", value="Experiencia:{self.xp}")
        embed.add_field(name="karma", value="Karma:{self.karma}")
        embed.set_footer(text="'''")
        await message.send(embed=embed)


    
    def addxp(self, file, dictionary):
        xp = random.randint(1,10)
        newxp = xp + self.xp
        if newxp < self.level * 10:
            self.xp = newxp 
        else:
            self.xp = newxp - self.xp * 10
            self.level += 1

    def addkarma(self, file, dictionary):
        self.karma += 1
    
    def rmkarma(self, file, dictionary):
        self.karma -= 1




