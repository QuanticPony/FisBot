from .classes.bot_class import FisBot

def context_is_admin(context):
    '''Devuelve True si el author del contexto que activa cierta funcion del Bot tiene permisos de administrador en dicho Servidor.
    Esta funcion se puede importar a otras extensiones para ponerla como check de commandos y cogs'''
    
    if context.guild:
        return context.message.author.guild_permissions.administrator
    else:
        return False