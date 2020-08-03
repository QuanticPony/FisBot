# Primero importamos el envoltorio de la api de discord. discord.py: https://discordpy.readthedocs.io/en/latest/
import discord

# Ahora importamos la clase (objeto) que envuelve al bot basico de discord. Esto quiere decir que tienes las mismas funciones que un
# bot normal y alguna extra que añadamos nosotros. En este caso he añadido funciones que permiten cargar y descargar conjuntos de archivos
# con comandos y funcionalidades extras
from bot_class import FisBot



# Creamos el objeto bot. Es de tipo FisBot (la clase envoltorio del bot de discord) creada por nosotros. Y le ponemos como prefijo el 
# caracter punto, porque me parece muy simple y rapido de poner
bot = FisBot(command_prefix='.')


# Aqui arrancamos el bot. Para ello leemos el archivo token.txt y lo guardamos en una variable token_file. Usamos la funcion de archivos de
# texto predefinida de python para convertirlo en una string (str) y se lo pasamos a bot.run(). Esta linea de comando debe estar siempre al
# final de todo, porque el resto no se leeria hasta que se finalizara el programa, y la idea es que no se finalice
with open("token.txt", "r") as token_file:
    bot.run(str(token_file.read()))


# La forma a la que estaras acostumbrado hacer lo anterior es la siguiente:
# file = open("token.txt", "r")
# token = str(file.read())
# bot.run(token)
# Son identicas, pero ya que estamos aprendiendo un nuevo lenguaje vamos a ponerlo chulo



# Si estas en Windows te recomiendo que tengas un archivo .cmd que ejecute el bot con un doble clic. El codigo seria asi:
# python run.py
# Deberia estar en el mismo directorio, si no deberias poner la ruta completa