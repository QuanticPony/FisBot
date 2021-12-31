import discord
import asyncio
import random
import pickle
from time import time
from discord.ext import commands


class HaceGracia(
    commands.Cog,
    name='EquisDe'
    ):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        pass_context=True, 
        brief='''Hace cuestiones''',
        description='''Donde esta?? No vemos esa mesa Arturo''',
        usage='.arturo [numero]'
    )
    async def arturo(self, context, *times):

        arturo = context.guild.get_member_named('Alfarceus#8109')
        if times == None:
                times = 1

        try:
            times = int(' '.join(times))
        except:
            times = 1

        if arturo:
            print(times)
            
            if times > 6:
                times = 6
            if times < 1:
                await context.send('.no puedes listillo')
                return
            for i in range(int(times)):
                await context.send(f"Donde esta la mesa {arturo.mention}?? Eh?? Donde esta??!!")

    @commands.command(
        pass_context=True, 
        brief='''Te felicita el nuevo año''',
        description='''felicesfiestasyfelizañonuevo.ojalaelsiguienteañonoseatanmalocomoeste''',
        usage='.newyear'
    )
    async def newyear(self, context):
        embed = discord.Embed(
            title='**felizañonuevo.mp4**',
            description='ḩ̵̼̪͗̓̇͆̌́̎́̍͐̑͆̃̾̕o̶̢̠̦̲̮͉̻̞̭̩̜͚̒͊̊̀̏͗̀͑͑͝ļ̴̧̛̲͔̯̹̯͙͇͚̘͈͛̔̿̔̒̋̌͘͜ã̴̡̛͎̩̮̥̣̣̳̺̲̫̹͔̇̇̋̉͊́̕ ̷̧͚̝̱̖̣͗͗͑̂̎̑͋̑͑͠͝ͅb̸̡̛̛͕͙͖͓̹̝̭̰͙̹͈̓̉͊̆̎͗͛̊̓̑̅̈̇u̷̡̬̫̥͎͓̺̫̭̠̣͌͑e̶̢̛̺̬̱̲͈̦͙͍̱͖̮̘̯͐̿͛͐̈́͛ň̸̙̞̭̹̅̈́̆̅͆̅̎̃̆a̴̮̩͉̘̮͚̦̗̜̫͇̘͐̒̔̔̅͂́͂̋́̆̿̕̕͝s̵̢͖̲̞̅̐̈́̋͑̌̽̚ ̷̨͕̥͚̼̺͕̣̱͓̪̬̞̲̽̒͐̚͘ẗ̸̡̳͓́͐̉a̸̛̹͗͋̊͛̈́̔̈́͒͂̇̏̒̚͠r̴͍͇͈̞̲̻̖̫͔̿̄̀̍͒̐͐̉̈́͌́̚̚d̴̡̢͍̖̼̥̦͙͙̠͍̟̩̦̐̈́́̈́̽̈́̈́̆͛͗́͑͜͝͠e̴̳̠͎͔̥̘̻̺̮̯͛̏͆͂̊͋̅͆̇̆̽͜͝ͅs̷͍̤̰͕̺̻̺͈̆̓͐̆́́̿̈́̀̿̊̔̃̚:̴̰̀ ̷̨̛̹͚̇͌͒͊̈́͋̈̊͌͗̑̿̌̒ḽ̶̥̤̮͎͒̏̑̀͛̓͊͂̊̏̄̂̋͆e̴̬̗̟͎̱͓͈͍͇͍̰̹̤̎́ͅͅs̸̹̲̝̯͈͇̣̮̉̾̎̾̓̚͠ͅ ̷̢̨͕̗͕̪̺̱̼̤̗̼̥̅͜d̴̨͉̜͈̭͓̠̦̪̰̺͆̋̒͑́̂̇͝è̴̢̢͙̖̝̖͍̺̦̘̅̔̀͜s̸̨̬̦͆́̑̄̐̅͠͝͝͠e̷̙̣̬̞̥̜̠̮̋͌̆̿͂̀ã̸̧̮͎̺͉͖͈͙̭̓̽͂́̒̕͝ͅm̸̢͇̱̬̤̺̂̎̈́͛̈́͑͆̿͆̄̒́̕͝o̷͎̜͉͇̮͔͈̥͍̦̰̥͖̤͋́͋̇̉̓̾͌͌̀͝ş̵̡̣̰̳̰̞̭̑́͒́ ̸̨̻̫̦͖̹̬͊̾͋͒̋́͂͂̒̔͜͠u̷̜̬̱̪̣̗̠̳̦̩͉̥͕̓͆̋͐̆͌n̵͉̟͈͚̹̥̼̣̠͇̪͊̓͛̅̑̽̈́̒̒͘̚͝ͅͅ ̴̡̢̬̜͓̝̟̟͈͙̞̥̂̊̇̅͑̋̐͑̂̂̿͝͝͠f̶̥̤̣͈̏͑̽͠͝ę̸̨̛̪̜̼̞͍͕̝̻̗̱̹̮̇̑́̉̄͐́͆̈́̔̒͜͠l̶̛͖̜̗͉̭͕͎͒̍̀̔̈̽̔̿͗̾̑͘͘͜i̸̛̙͙̼̝̼̤̪̖̘̐͆̃̍̉͗̾̋̓̾͐͑̿͘ż̴̢̢̛͈̪͔̻̫̩̼̝̼̰̣̳̠̈ ̷̧̢̛̞̼̝̣̩̙̦̺̉͐̂̊̓́̓̏́̍̏͘͜͝a̴̧̢̟͖̣̜̖͎͉͑̀̍̌̈́̎̾͘͝ñ̷̢̠̻̮̲͖̤͇̹̞͒̂̀̏̏̅̓̇̚͘͜͜ͅͅo̸̦̘̳̭̳͊́̌̉̐́̆̓̀͜͜ ̴̨̜̼̈́̔͗̔̎̏̍̀̈͌͌̒̑͠n̸̘̼͍̠̖͎̘̐̇̈̀͐̒͛͐̿͂͑͒̈̋u̸̡̡̡̱̖̲̦̣̼̬̘̦̩͊̍ĕ̷͋̐̾̇̑̐̕͘ͅv̸̡̨͚̠̬͇̳̣͇̜͈̭̌̂̉̒̂̽͛͌̂̈̍̎ǫ̴̡̣̱͍̟͎͈͇̘͓͉̰̰͆͋̌̿̕͘͜͝ ',
            color=discord.Color.dark_magenta())
        embed.add_field(name='Que este año no sea tan basura gracias', value='[Te deseamos lo mejor♥](https://youtu.be/EUs956xdIfE?t=12)')
        embed.set_footer(text='Y unas campanitas para que te arruinen la tarde', icon_url='https://c0.klipartz.com/pngpicture/73/708/gratis-png-campana.png')
        await context.send(embed=embed)


    @commands.command(
        pass_context=True, 
        brief='''eco eco eco...''',
        description='''eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco eco...''',
        usage='.eco [persona] [vocal]'
    )
    async def eco(self, context, *vocal):

        for letra in vocal:
            if len(letra)==1:
                vocal = letra
                break
        else:
            vocal = None
        mentions = context.message.mentions
        if not mentions:
            mentions = [context.author]

        check_user = lambda message: not message.author.bot and message.author in mentions

        time_start = time()
        time_finish = time_start + 30

        for i in range(10):
            try:
                timeout = time_finish-time_start
                msg = await self.bot.wait_for('message', timeout= timeout if timeout > 0 else 1, check=check_user)
                text = msg.content
                if vocal:
                    text = text.replace('a', vocal)
                    text = text.replace('e', vocal)
                    text = text.replace('i', vocal)
                    text = text.replace('o', vocal)
                    text = text.replace('u', vocal)
                await context.send(text)
            except asyncio.TimeoutError:
                return