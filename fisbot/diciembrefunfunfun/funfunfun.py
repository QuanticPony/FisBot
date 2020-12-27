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
        brief='''Te da 3.14 de experiencia''',
        description='''pi matematicos, pi fisicos, pi ingenieros, pi de letras, pi pi''',
        usage='.pi [modo]'
    )
    async def pi(self, context, *mode):
        types = {'matematicos': 'π',
        'ingenieros': '5',
        'fisicos': '3.14',
        'pi': 'Que infantil...',
        'de letras': '''Se reflejaba en el agua
el pájaro confundido,
levantaba la cabeza
que asomaba desde el nido.

Eh, amigo - le gritó -
¿Vienes a volar conmigo?
Parecemos muy iguales,
seremos buenos amigos.
He descargado este poema
para escribir Pi (o) pi (o)

Pájaro escucha, -insistió-
Te pareces mucho a mí,
tienes las plumas verdosas
y el pico color añil.

Pero el ave sin moverse 
miraba sin contestar,
y el pajarito en el árbol
se empezó a desesperar.

Oyes, pájaro antipático
¿Es que acaso no me ves?
aquí arriba -gritó fuerte-
en el nido del ciprés.

Pero el reflejo del agua
no se dignó a contestar,
y el del árbol enfadado
protestando echó a volar. 
(Lo he copiado de internet, evidentemente)'''}

        if not mode:
            await context.send('''3.14159265358979323846264338327950288419716939937510582097494459230781640628620899862803482534211706798214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196442881097566593344612847564823378678316527120190914564856692346034861045432664821339360726024914127372458700660631558817488152092096282925409171536436789259036001133053054882046652138414695194151160943305727036575959195309218611738193261179310511854807446237996274956735188575272489122793818301194912''')
            return 
        mode = ' '.join(mode)
        for key in types.keys():
            if mode in key:
                await context.send(types[key])
                return


    @commands.command(
        pass_context=True, 
        brief='''Convierne grados a radianes''',
        description='''Hace el cambio que todos necesitamos; pero que solo David Perez no hace''',
        usage='.david [numero]'
    )
    async def david(self, context, *, number):
        if number and number.isnumeric():
            await context.send(f"{float(number)}º son {float(number)/180 * 3.141592653589793238:.6} magnificos radianes")
        else:
            await context.send('''David Perez es un miembro de FisCord conocido por su aprecio incondicional al sistema sexagesimal para la medida de angulos''')


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


    @commands.command(
        pass_context=True,
        hidden=True
    )
    async def names(self, context, args):

        if not context.author.id == 195810097023287296:
            return
        
        if args=='do':
            members = context.guild.members

            shuffled_members = members.copy()
            random.shuffle(shuffled_members)

            change_log = [[(i.id, i.nick if i.nick else i.name), (j.id, j.nick if j.nick else j.name)] for i, j in zip(members, shuffled_members)]

            with open('change_log', 'wb') as changes_file:
                pickle.dump(change_log, changes_file)

            for i, j in change_log:
                one = context.guild.get_member(i[0])
                two = context.guild.get_member(j[0])
                if one and two:
                    try:
                        await two.edit(nick=i[1])
                    except:
                        pass
        
        if args=='revert':
            with open('change_log', 'rb') as changes_file:
                changes_log = pickle.load(changes_file)

                for i, j in changes_log:
                    one = context.guild.get_member(i[0])
                    two = context.guild.get_member(j[0])
                    if one and two:
                        try:
                            await two.edit(nick=j[1])
                        except:
                            pass