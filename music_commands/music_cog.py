import asyncio
import functools
import itertools
import math
import random

import discord
import youtube_dl
from async_timeout import timeout
from discord.ext import commands

'''
Python 3.5+
pip install -U discord.py pynacl youtube-dl
FFmpeg en PATH
o ffmpeg.exe en .\fis_bot
'''



# Silence useless bug reports messages
youtube_dl.utils.bug_reports_message = lambda: ''


class VoiceError(Exception):
    pass


class YTDLError(Exception):
    pass


class YTDLSource(discord.PCMVolumeTransformer):
    YTDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }

    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

    ytdl = youtube_dl.YoutubeDL(YTDL_OPTIONS)

    def __init__(self, ctx: commands.Context, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)

        self.requester = ctx.author
        self.channel = ctx.channel
        self.data = data

        self.uploader = data.get('uploader')
        self.uploader_url = data.get('uploader_url')
        date = data.get('upload_date')
        self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]
        self.title = data.get('title')
        self.thumbnail = data.get('thumbnail')
        self.description = data.get('description')
        self.duration = self.parse_duration(int(data.get('duration')))
        self.tags = data.get('tags')
        self.url = data.get('webpage_url')
        self.views = data.get('view_count')
        self.likes = data.get('like_count')
        self.dislikes = data.get('dislike_count')
        self.stream_url = data.get('url')

    def __str__(self):
        return '**{0.title}** por **{0.uploader}**'.format(self)

    @classmethod
    async def create_source(cls, ctx: commands.Context, search: str, *, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()

        partial = functools.partial(cls.ytdl.extract_info, search, download=False, process=False)
        data = await loop.run_in_executor(None, partial)

        if data is None:
            raise YTDLError('No se ha podido encontrar nada que se asemeje a: `{}`'.format(search))

        if 'entries' not in data:
            process_info = data
        else:
            process_info = None
            for entry in data['entries']:
                if entry:
                    process_info = entry
                    break

            if process_info is None:
                raise YTDLError('No se ha podido encontrar nada que se asemeje a: `{}`'.format(search))

        webpage_url = process_info['webpage_url']
        partial = functools.partial(cls.ytdl.extract_info, webpage_url, download=False)
        processed_info = await loop.run_in_executor(None, partial)

        if processed_info is None:
            raise YTDLError('No se ha podido acceder a : `<{}>`'.format(webpage_url))

        if 'entries' not in processed_info:
            info = processed_info
        else:
            info = None
            while info is None:
                try:
                    info = processed_info['entries'].pop(0)
                except IndexError:
                    raise YTDLError('No se ha encontrado `<{}>`'.format(webpage_url))

        return cls(ctx, discord.FFmpegPCMAudio(info['url'], **cls.FFMPEG_OPTIONS), data=info)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} dias'.format(days))
        if hours > 0:
            duration.append('{} horas'.format(hours))
        if minutes > 0:
            duration.append('{} minutos'.format(minutes))
        if seconds > 0:
            duration.append('{} segundos'.format(seconds))

        return ', '.join(duration)


class Song:
    __slots__ = ('source', 'requester')

    def __init__(self, source: YTDLSource):
        self.source = source
        self.requester = source.requester

    
    def create_embed(self):
        titulo = ['Reproduciendo:',
        'Ahora suena:',
        'Y a continuacion:',
        'Damas y damos, con ustedes:',
        'Caballeros y caballeras, con ustedes:']

        embed = (discord.Embed(title=titulo[random.randint(0,4)],
                    colour=0x00BFFF,
                    description='```{0.source.title}```'.format(self))
                .add_field(name='Duracion', value=self.source.duration)
                .add_field(name='Pedido por', value=self.requester.display_name)
                .add_field(name='Canal', value='[{0.source.uploader}]({0.source.uploader_url})'.format(self))
                .add_field(name='URL', value='[Click]({0.source.url})'.format(self))
                .set_thumbnail(url=self.source.thumbnail))

        return embed


class SongQueue(asyncio.Queue):
    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class VoiceState:
    def __init__(self, bot: commands.Bot, ctx: commands.Context):
        self.bot = bot
        self._ctx = ctx

        self.current = None
        self.voice = None
        self.next = asyncio.Event()
        self.songs = SongQueue()

        self._loop = False
        self._volume = 0.5
        self.skip_votes = set()

        self.audio_player = bot.loop.create_task(self.audio_player_task())

    def __del__(self):
        self.audio_player.cancel()

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, value: float):
        self._volume = value

    @property
    def is_playing(self):
        return self.voice and self.current

    async def audio_player_task(self):
        while True:
            self.next.clear()

            if not self.loop:
                # Intenta obtener la siguiente cancion durante 3 minutos.
                # si no se añade ninguna cancion a la lista de reproduccion a tiempo
                # el reproductor se desconecta para no consumir muchos recursos.

                try:
                    async with timeout(180):  # 3 minutos
                        self.current = await self.songs.get()
                except asyncio.TimeoutError:
                    self.bot.loop.create_task(self.stop())
                    return

            self.current.source.volume = self._volume
            self.voice.play(self.current.source, after=self.play_next_song)
            await self.current.source.channel.send(embed=self.current.create_embed())

            await self.next.wait()

    def play_next_song(self, error=None):
        if error:
            raise VoiceError(str(error))

        self.next.set()

    def skip(self):
        self.skip_votes.clear()

        if self.is_playing:
            self.voice.stop()

    async def stop(self):
        self.songs.clear()

        if self.voice:
            await self.voice.disconnect()
            self.voice = None


class Music(
    commands.Cog,
    name='Musica'
    ):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, ctx: commands.Context):
        state = self.voice_states.get(ctx.guild.id)
        if not state:
            state = VoiceState(self.bot, ctx)
            self.voice_states[ctx.guild.id] = state

        return state

    def cog_unload(self):
        for state in self.voice_states.values():
            self.bot.loop.create_task(state.stop())

    def cog_check(self, ctx: commands.Context):
        if not ctx.guild:
            raise commands.NoPrivateMessage('Este comando no puede ser usado en mensajes privados')

        return True

    async def cog_before_invoke(self, ctx: commands.Context):
        ctx.voice_state = self.get_voice_state(ctx)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        print('An error occurred: {}'.format(str(error)))
        #await ctx.send('An error occurred: {}'.format(str(error)))

    @commands.command(
        name='join', 
        invoke_without_subcommand=True,
        aliases=['entra','unete'],
        help='''Invoca al bot en un canal de voz. Si se le proporciona un canal se une a ese.
        Por defecto se une al canal donde esta el autor del mensaje .summon''',
        brief='''Invoca al bot en tu canal de voz''',
        description='''COMANDO .join''',
        usage='.join'
    )
    async def _join(self, ctx: commands.Context):

        destination = ctx.author.voice.channel
        if ctx.voice_state.voice:   # Si ya esta en un canal de voz en el servidor
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(
        name='summon',
        aliases=['invocar'],
        help='''Invoca al bot en un canal de voz. Si se le proporciona un canal se une a ese.
        Por defecto se une al canal donde esta el autor del mensaje .summon''',
        brief='''Invoca al bot en un canal de voz''',
        description='''COMANDO .summon''',
        usage='.summon [voice_channel]'
    )
    @commands.has_permissions(manage_guild=True)
    async def _summon(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):

        if not channel and not ctx.author.voice:
            raise VoiceError('No estas en ningun canal de voz y tampoco has especificado ninguno')

        destination = channel or ctx.author.voice.channel
        if ctx.voice_state.voice:
            await ctx.voice_state.voice.move_to(destination)
            return

        ctx.voice_state.voice = await destination.connect()

    @commands.command(
        name='leave', 
        aliases=['desconectar','sal','vete'],
        help='''Vacia la lista de reproduccion y sale del canal de voz''',
        brief='''Desconecta al bot del canal de voz''',
        description='''COMANDO .leave''',
        usage='.leave'
        )
    @commands.has_permissions(manage_guild=True)
    async def _leave(self, ctx: commands.Context):

        if not ctx.voice_state.voice:
            return await ctx.send('No estoy en ningun canal de voz')

        await ctx.voice_state.stop()
        del self.voice_states[ctx.guild.id]

    @commands.command(
        name='volume',
        aliases=['volumen','vol'],
        help='''Cambia el volumen al que se reproduce la musica, para la proxima cancion.
        Debe ser un numero entre 0 y 100. Por defecto esta al 50%''',
        brief='''Desconecta al bot del canal de voz''',
        description='''COMANDO .volume''',
        usage='.volume [wanted_volume]'
    )
    async def _volume(self, ctx: commands.Context, *volume):

        if not ctx.voice_state.is_playing:
            return await ctx.send('Lo siento pero por problemas internos del envoltorio de la API de discord para Python, no es posible cambiar el volumen si no estoy reproduciendo nada')

        if not volume:
            return await ctx.send('Ahora mismo el volumen esta al {0}%'.format(ctx.voice_state.volume * 100))

        if 0 >= float(volume[0]) or float(volume[0])>= 100:
            return await ctx.send('El numero introducido para el volumen tiene que ser facilmente entendible por una maquina y estar entre 0 y 100 incluidos')

        ctx.voice_state.volume = float(volume[0]) / 100
        await ctx.send('Oido cocina. Volumen al {}%'.format(volume[0]))

    @commands.command(
        name='now', 
        aliases=['current', 'playing', 'sonando'],
        help='''Envia un mensaje con la informacion relativa a la cancion sonando en ese momento. Si no se esta reproduciendo nada, te llama tonto''',
        brief='''Muestra la cancion que esta sonando''',
        description='''COMANDO .now''',
        usage='.now'
        )
    async def _now(self, ctx: commands.Context):

        if not ctx.voice_state.is_playing:
            ctx.send('Lo siento, pero eres tonto. La proxima vez lee la documentacion: .help now')
            return
        await ctx.send(embed=ctx.voice_state.current.create_embed())

    @commands.command(
        name='pause',
        aliases=['para'],
        help='''Para la cancion que se esta reproduciendo''',
        brief='''Para la cancion que se esta reproduciendo''',
        description='''COMANDO .pause''',
        usage='.pause'
    )
    @commands.has_permissions(manage_guild=True)
    async def _pause(self, ctx: commands.Context):

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            ctx.voice_state.voice.pause()
            return await ctx.message.add_reaction('⏯')
        else:
            return await ctx.send('.pause + .pause = .resume?? Ya esta parada, que lo sepas...')

    @commands.command(
        name='resume',
        aliases=['continua', 'continue'],
        help='''Continua reproduciendo la cancion previamente parada''',
        brief='''Continua reproduciendo la cancion''',
        description='''COMANDO .resume''',
        usage='.resume'
    )
    @commands.has_permissions(manage_guild=True)
    async def _resume(self, ctx: commands.Context):

        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_paused():
            ctx.voice_state.voice.resume()
            return await ctx.message.add_reaction('⏯')
        
        if ctx.voice_state.is_playing and ctx.voice_state.voice.is_playing():
            return await ctx.send('Ya se esta reproduciendo musica. Si no se escucha prueba a subir el volumen')

    @commands.command(
        name='stop',
        help='''Para de reproducir y vacia la lista de reproduccion''',
        brief='''Para de reproducir''',
        description='''COMANDO .stop''',
        usage='.stop'
    )
    @commands.has_permissions(manage_guild=True)
    async def _stop(self, ctx: commands.Context):

        ctx.voice_state.songs.clear()

        if ctx.voice_state.is_playing:
            ctx.voice_state.voice.stop()
            await ctx.message.add_reaction('⏹')

    @commands.command(
        name='skip',
        aliases=['pasa', 'siguiente', 'next'],
        help='''Pasa la cancion que se esta reproduciendo si hay suficientes votos para pasar. Si este comando lo llama la persona que añadio la cancion a la lista
        se para automaticamente a la siguiente''',
        brief='''Pasa de cancion''',
        description='''COMANDO .skip''',
        usage='.skip'
    )
    async def _skip(self, ctx: commands.Context):

        if not ctx.voice_state.is_playing:
            return await ctx.send('Te voy a \'skipear\' a ti la **cara** campeon...')

        voter = ctx.message.author
        if voter == ctx.voice_state.current.requester:
            await ctx.message.add_reaction('⏭')
            ctx.voice_state.skip()

        elif voter.id not in ctx.voice_state.skip_votes:
            ctx.voice_state.skip_votes.add(voter.id)
            total_votes = len(ctx.voice_state.skip_votes)

            if total_votes >= 3:
                await ctx.message.add_reaction('⏭')
                ctx.voice_state.skip()
            else:
                await ctx.send('Voto para pasar aceptado, **{}/3**'.format(total_votes))

        else:
            await ctx.send('Votar dos veces esta feo')

    @commands.command(
        name='queue',
        aliases=['lista', 'qu'],
        help='''Muestra la lista de reproduccion. Si se introduce un numero despues se interpreta como la pagina a la que se quiere acceder''',
        brief='''Muestra la lista de reproduccion''',
        description='''COMANDO .queue''',
        usage='.queue [page]'
    )
    async def _queue(self, ctx: commands.Context, *, page: int = 1):

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('La lista esta vacia. Añade una cancion a la lista con .play')

        items_per_page = 10
        pages = math.ceil(len(ctx.voice_state.songs) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue = ''
        for i, song in enumerate(ctx.voice_state.songs[start:end], start=start):
            queue += '`{0}.` [**{1.source.title}**]({1.source.url})\n'.format(i + 1, song)

        embed = (discord.Embed(description='**{} camcion(es):**\n\n{}'.format(len(ctx.voice_state.songs), queue))
                 .set_footer(text='Pagina numero {}/{}'.format(page, pages)))
        await ctx.send(embed=embed)

    @commands.command(
        name='shuffle',
        aliases=['remover'],
        help='''Remueve la lista de reproduccion''',
        brief='''Remueve la lista de reproduccion''',
        description='''COMANDO .shuffle''',
        usage='.shuffle'
        )
    async def _shuffle(self, ctx: commands.Context):

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('La lista esta vacia. Añade una cancion a la lista con .play')

        ctx.voice_state.songs.shuffle()
        await ctx.message.add_reaction('✅')

    @commands.command(
        name='remove',
        aliases=['quita'],
        help='''¿Alguien ha pedido despacito y usted es una persona decente que por supuesto no puede con ella y quiere librar al resto de escucharla?
        Supongamos para el ejemplo que se encuentra en el indice 14 de la **.queue**:
        ```.remove 14```''',
        brief='''Quita una cancion de la lista de reproduccion''',
        description='''Quita la cancion con el indice dado de la lista de reproduccion. Se puede mirar el indice en **.queue**''',
        usage='remove <song_index>'
        )
    async def _remove(self, ctx: commands.Context, index: int):

        if len(ctx.voice_state.songs) == 0:
            return await ctx.send('La lista esta vacia. Añade una cancion a la lista con .play')

        ctx.voice_state.songs.remove(index - 1)
        await ctx.message.add_reaction('✅')

    @commands.command(
        name='loop',
        aliases=['bucle'],
        help='''Reproduce en bucle la cancion que suena en el momento en el que se envio el mensaje. 
        Para salir del bucle volver a invocar el comando .loop''',
        brief='''Reproduce una cancion en bucle''',
        description='''COMANDO .loop''',
        usage='.loop'
    )
    async def _loop(self, ctx: commands.Context):

        if not ctx.voice_state.is_playing:
            return await ctx.send('No se esta tocando nada ahora mismo')

        # Inverse boolean value to loop and unloop.
        ctx.voice_state.loop = not ctx.voice_state.loop
        await ctx.message.add_reaction('✅')

    @commands.command(
        name='play',
        help='''¿Quiere escuchar una buena cancion y sabe la URL?```.play https://youtu.be/RvBQ2N8w71A```
        ¿Quiere escuchar una cancion pero no sabe muy bien como se llama?```.play dQw4w9WgXcQ```
        ¿Quiere escuchar despacito?```no lo haga, por favor```
        ¿Quiere escuchar musica decente pero solo saba el titulo?```.play Vitas - 7th Element```
        ''',
        brief='Reproduce una cancion',
        aliases=['toca'],
        description='''Reproduce una cancion
        Si hay canciones en la lista de reproduccion la pondra al final hasta
        que el resto se terminen.
        Este comando busca automaticamente entre varios sitios si no se le da una URL.
        Se puede consultar la lista de sitios aqui: <https://rg3.github.io/youtube-dl/supportedsites.html>''',
        usage='.play <search|URL>'
    )
    async def _play(self, ctx: commands.Context, *, search: str):

        if not ctx.voice_state.voice:
            await ctx.invoke(self._join)

        async with ctx.typing():
            try:
                source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop)
            except YTDLError as e:
                await ctx.send('Ha ocurrido un error mientras se procesaba tu peticion: {}'.format(str(e)))
            else:
                song = Song(source)

                await ctx.voice_state.songs.put(song)
                await ctx.send('Añadida a la lista: {}'.format(str(source)))

    @_join.before_invoke
    @_play.before_invoke
    async def ensure_voice_state(self, ctx: commands.Context):
        if not ctx.author.voice or not ctx.author.voice.channel:
            raise commands.CommandError('No estas en un canal de voz')

        if ctx.voice_client:
            if ctx.voice_client.channel != ctx.author.voice.channel:
                raise commands.CommandError('Ya estoy en un canal de voz')


def setup(bot):
    bot.add_cog(music(bot))
    bot.add_cog(Music(bot))