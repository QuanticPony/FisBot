from .classes.bot_class import FisBot, FisBotServer
import logging

def context_is_admin(context):
    '''Devuelve True si el author del contexto que activa cierta funcion del Bot tiene permisos de administrador en dicho Servidor.
    Esta funcion se puede importar a otras extensiones para ponerla como check de commandos y cogs'''
    
    if context.guild:
        if context.author.guild_permissions.administrator:
            return True
        
        for r in context.author.roles:
            if 'Mods' in r.name:
                return True
        return False

    else:
        return False
    
def context_is_whitelisted(context):
    '''Devuelve True si el author del contexto que activa cierta funcion del Bot está en el archivo whitelist.txt.
    Esta funcion se puede importar a otras extensiones para ponerla como check de commandos y cogs'''


    with open("whitelist.txt", "r") as file:
        for line in file:
            if int(line.split("=")[-1]) == context.author.id:
                logging.info(f"User {context.author.name} was found on whitelist")
                return True
            
        logging.info(f"User {context.author.name} was not found on whitelist")
        return False
        
    