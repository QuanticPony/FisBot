import discord
import asyncio
from discord.ext import commands

from bot_class import context_is_admin


def setup(bot):
    bot.add_cog(__pruebas(bot))



class __pruebas(
    commands.Cog,
    name='Pruebas' 
    ):
    '''Esto es una descripcion poco descriptiva en la que utilizo ```lineas de codigo del propio discord``` Asi como **negrita** y *cursiva*'''

    def __init__(self, bot):
        self.bot = bot 


    @commands.command(
        pass_context=True,  
        hidden=False,       
        name='hola',        
        aliases=['hello','andiamo','hallo'],
        help='''¿Acaba usted de conectarse? ```.holla```
        ¿Quiere saludar a alguien? ```.hallo Pablo```
        ¿Quiere saludar a un grupo?```.andiamo @mods```''',                                                 
        brief='''Saluda''', 
        description='''Elimina [amount] mensajes. Por defecto elmina el enviado y el anterior''',   
        usage='.hello [person|group|roll]',   
        checks=[context_is_admin]                 
    ) 
    async def __hola(self, context, *, seres):

        async def _rehola(context):
            await context.send('Hola')

        if not seres:
            await _rehola(context)
            return
        
        if context.message.mention_everyone:
            await context.send('Hola @everyone')
            return

        with personas_mencionadas as context.message.mentions:
            if personas_mencionadas:   
                for persona in personas_mencionadas:
                    await context.send('Hola {.mention}'.format(persona))
                else:
                    return

        for persona in seres:
            await context.send('Hola ' + persona)
            return


        
