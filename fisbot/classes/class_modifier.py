import discord
import asyncio
from discord.ext import commands

async def modify(obj: object, ctx: commands.Context, *,
    role=False,
    task=False,
    user=False,

) -> bool:
    '''Permite modificar una clase generica de forma sencilla a traves de una interfaz visual a base de mensajes `discord.Embed` por mensajes individuales'''

    atributes_dic = obj.__dict__.copy()

    channel = ctx.author.dm_channel
    if not channel:
        channel = await ctx.author.create_dm()

    if role:
        disc_obj = ctx.guild.get_role(obj.id)
    elif task:
        disc_obj = obj
    elif user:
        disc_obj = ctx.guild.get_member(obj.id)
    else:
        return False


    embed = discord.Embed(
        title=obj._mod_title(),
        description=obj._mod_desc(),
        color=discord.Color.dark_green()
    )


    atributes_dic.pop('id')
    atributes_dic.pop('database')
    try:
        atributes_dic.pop('mention')
    except KeyError:
        pass

    codepoint_start = 127462  # Letra A en unicode en emoji
    things_list = {f"{chr(i)}": v for i, v in enumerate(atributes_dic, start=codepoint_start)}

    message = await channel.send(embed=embed)
    for i in range(len(things_list)):
        await message.add_reaction(chr(i+codepoint_start)) 
    await message.add_reaction("💾")

    async def _re_embed():
        embed.clear_fields()
        for atrib in things_list:
            embed.add_field(
                name=f"{atrib} - {things_list[atrib]}:" ,
                value=obj.__dict__[things_list[atrib]],
                inline=False
                )
        await message.edit(embed=embed)


    async def _ask_field() -> bool:
        '''Esta funcion se encarga de preguntar una y otra vez si se quiere cambiar algun campo y cual'''

        await _re_embed()

        try:
            reaction, user = await ctx.bot.wait_for('reaction_add', timeout=15.0)
            if str(reaction.emoji) == '💾':
                return False
                
        except asyncio.TimeoutError:
            await channel.send('Se acabo el tiempo...')
            return False

        ask_message = await channel.send(f"Introduce un nuevo {things_list[reaction.emoji]}:")

        try:
            response_msg = await ctx.bot.wait_for('message', timeout=120.0)
        except asyncio.TimeoutError:
            await channel.send('Se acabo el tiempo...')
            return False
          
        setattr(obj, things_list[reaction.emoji], response_msg.content)
        await response_msg.add_reaction("✅")
        await ask_message.delete()
        return True

        

    while await _ask_field():
        pass
    await _re_embed()

    if role:
        obj.database.update_rol(obj)
    elif task:
        obj.database.update_task(obj)
    elif user:
        obj.database.update_user(obj)
    
    return True