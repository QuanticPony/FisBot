# Estos imports son las librerias basicas que debe tener cualquier extension
import discord
import asyncio
from discord.ext import commands

# Esta funcion la importo solo por interes demostrativo mas adelante
from bot_class import context_is_admin


# Al utilizar extensiones de la api de discord hay que usar sus normas. son las siguientes:
# Toda extension tiene que tener una funcion setup definida. La suelo definir al final, pero la voy a poner aqui al principio para que se vea.
# Su funcion es inicializar el objeto que sera la extension requerida:
def setup(bot):
    bot.add_cog(__pruebas(bot))

# Por si no os habeis mirado la api: commands.Cog es un objeto que implementa una categoria de comandos. Se añaden al bot con la funcion
# commands.Bot.add_cog(<cog_class>.__init__([argumentos]))
# Si poneis el nombre de la clase y los argumentos depues como lo he puesto arriba no hace falta llamar a la funcion __init__. Se presupone


# Ahora vamos a definir el objeto que sera la extension. Como es una categoria de comandos debe heredar de commands.Cog:
class __pruebas(
    commands.Cog,
    name='Pruebas' 
    # Esto no es extrictamente necesario. Si no estuviera el nombre de la categoria seria el nombre de la clase, pero para
    # dejar todo mas bonito no nos cuesta nada. Y asi habra menos problemas de llamar a las cosas iguales.
    ):
    # Ahora hay que escribir la descripcion del conjunto de comandos, hay que ponerla seguida como si fuera una linea de codigo, asi mismo:
    '''Esto es una descripcion poco descriptiva en la que utilizo ```lineas de codigo del propio discord``` Asi como **negrita** y *cursiva*'''


    # Esta es la definicion de la creacion de la clase. Queremos saber cual es el bot, asi que se lo pasamos y lo guardamos como atributo:
    def __init__(self, bot):
        self.bot = bot # Guardado. Ahora si queremos acceder dentro de las funciones definidas en esta clase habria que escribir self.bot.(lo que queramos)



    # Definamos ahora un comando basico, siempre hay que hacerlo asi 
    # Hay muchas cosas que le podeis poner a un comando a parte de lo que hace el mismo. Aqui os pongo un comando completo
    # del cual tendriais que quitar aquellas partes que no os interesen:
    @commands.command(
        pass_context=True,  # Si quereis que se le pase al comando un objeto (discord.Context) que nos indica en que condiciones se ha invocado este comando
        hidden=False,       # Si quereis que se muestre o no en el comando .help. Ponedlo siempre en False a no ser que sea algo muy secreto
        name='hola',        # Nombre basico del comando y por el cual se le llama en discord
        aliases=['hello','andiamo','hallo'],  #Lista de nombres alternativos por los cuales tambien se puede llamar al comando

        help='''¿Acaba usted de conectarse? ```.holla```
        ¿Quiere saludar a alguien? ```.hallo Pablo```
        ¿Quiere saludar a un grupo?```.andiamo @mods```''', # Esto se podria utilizar de otra forma, pero con la implementacion custom que hay de .help
                                                            # ponemos ejemplos de utilizacion

        brief='''Saluda''', # Breve descripcion que saldra al poner .help sin nada mas. Suele ser la descripcion siguiente reducida

        description='''Elimina [amount] mensajes. Por defecto elmina el enviado y el anterior''',   #Descripcion de lo que hace el comando

        usage='.hello [person|group|roll]',    # Descripcion de como se usa el comando. Suelo usar [] para opcional y <> para obligarior

        checks=[context_is_admin]   # Tienes que pasarle una lista de funciones que comprueban si se puede ejecutar el comando. Normalmente el check sera si el 
                                    # usuario es administrador, como este caso, que hemos puesto la funcion importada anteriormente
    ) 
    # Ahora vendria la propia definicion del comando. Es parecido a c en la definicion, lo unico que el primer parametro tiene que ser siempre self y el segundo 
    # suele ser el contexto 
    # El async hace que se puede ejecutar a la vez que otra cosa = asincronia. Despues hay que poner algun await
    async def __hola(self, context, *, seres):
        # Si poneis un asterisco asi y despues algo lo que decis es que todo lo que pongais despues del comando se guarda como una lista en seres

        # Se pueden definir funciones dentro de funciones. Este es un ejemplo muy tonto que mira a ver si se ha nombrado un rol en el mensaje:
        async def _rehola(context):
            await context.send('Hola')
            # await hace que se haga eso cuando se pueda. Para enviar mensajes siempre hay que ponerlo

        if not seres:   # Si no se escribe nada te dice hola
            await _rehola(context)
            return


        if context.message.mention_everyone:    # Si se menciona a todo el mundo
            await context.send('Hola @everyone')
            return

        with personas_mencionadas as context.message.mentions:
        # Lista de menciones en el mensaje del contexto que ha invocado el comando. Hay que leer al reves para entenderlo bien
        # Si no hay menciones estara vacia. Para ver si esta con algo:
                if personas_mencionadas: # Si no esta vacia
                    for persona in personas_mencionadas:
                        # Enviamos un mensaje por cada persona mencionada:
                        await context.send('Hola {.mention}'.format(persona))
                        # Si quereis algo mas parecido a c:
                        # await context.send(str('Hola %s', persona.mention))
                        # Es altamente preferible la primera
                    else: # Si se cumple completamente el bucle for
                        return

        # Si se escribe el nombre de alguien pero no se le menciona
        for persona in seres:
            await context.send('Hola ' + persona)
            return
