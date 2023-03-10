import nextcord
from nextcord.ext import commands
from nextcord.shard import EventItem
import wavelink

bot_version = "0.0.1"

intents = nextcord.Intents.all()
client = nextcord.Client()
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print("Bot Ready!")
    bot.loop.create_task(on_node())

# This function joins a LavaLink Host
async def on_node():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host="node1.kartadharta.xyz", password="kdlavalink", port=443, https=True)

# Calls when the song finishes and plays the next song or disconnects
@bot.event
async def on_wavelink_track_end(player : wavelink.Player, track : wavelink.Track, reason):

    ctx = player
    vc: player = ctx.guild.voice_client

    if not player.queue.is_empty:
        next_song = vc.queue.get()
        await vc.play(next_song)
    else:
        return await vc.disconnect()

@bot.slash_command(guild_ids=[708632631901683723], description="About the Bot")
async def about(interaction : nextcord.Interaction):

    em = nextcord.Embed(title="About The Bot") # IF QUEUE IS NOT EMPTY SEND AN EMBED
    em.add_field(name=f"BoomBot", value=f"A simple music bot for all your music needs.", inline=False)
    em.add_field(name=f"Version", value=f"{bot_version}", inline=False)
    em.add_field(name=f"Creator", value="Zyb3rWolfi", inline=False)

    await interaction.response.send_message(embed=em)

# Searches a song on Youtube and plays it through the VC
@bot.slash_command(guild_ids=[708632631901683723], description="Search For a Song")
async def play(interaction : nextcord.Interaction, search : str):

    query = await wavelink.YouTubeTrack.search(query=search, return_first=True)
    try:
        destination = interaction.user.voice.channel

        if not interaction.guild.voice_client:

            vc: wavelink.Player = await destination.connect(cls=wavelink.Player)
        elif interaction.guild.voice_client:

            vc: wavelink.Player = interaction.guild.voice_client
    
    except:
        await interaction.response.send_message("Join a VC First!")
    
    if vc.queue.is_empty and not vc.is_playing():

        await vc.play(query)
        await interaction.response.send_message(f"Now Playing {query.title} {query.uri}")
    
    else:
        await vc.queue.put_wait(query)
        await interaction.response.send_message(f"Added {query.title} To the Queue")

# Skips the current song by stopping it and then "on_wavelink_track_end" starts the next song
@bot.slash_command(guild_ids=[708632631901683723], description="Skip the current song")
async def skip(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client

    if not vc.queue.is_empty:

        await vc.stop()
        await interaction.response.send_message("Song skipped!")
    else:

        await interaction.response.send_message("Cant Skip! There is nothing in the Queue")

# Shows the current queue in an embed for the user
@bot.slash_command(guild_ids=[708632631901683723], description="Shows the current Queue")
async def queue(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client # SETS THE PLAYER
    if not vc.queue.is_empty:
        em = nextcord.Embed(title="Queue") # IF QUEUE IS NOT EMPTY SEND AN EMBED
        queue = vc.queue.copy()
        songs = []
        song_count = 0
        for song in queue:
            song_count += 1
            songs.append(song)
            em.add_field(name=f"[{song_count}] Duration {song.duration}", value=f"{song.title}", inline=False)

        await interaction.response.send_message(embed=em)
    else:
        await interaction.response.send_message("Queue is empty!")

# Disconnects the user from the channel
@bot.slash_command(guild_ids=[708632631901683723], description="Disconnects the bot from a VC")
async def disconnect(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client
    await vc.disconnect()
    await interaction.response.send_message("Disconnected the Bot")

# Pauses the current song
@bot.slash_command(guild_ids=[708632631901683723], description="Pause a song")#
async def pause(interaction : nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    try:
        await vc.pause()
        await interaction.response.send_message("Paused the current song")
    except:
        await interaction.response.send_message("Song is already Pasued!")

# Resumes the current song
@bot.slash_command(guild_ids=[708632631901683723], description="Pause a song")
async def resume(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client
    try:      
        await vc.resume()
        await interaction.response.send_message("Resumed the current song")
    except:
        await interaction.response.send_message("Song is already resumed!")

# Shows what song is currently playing
@bot.slash_command(guild_ids=[708632631901683723], description="Shows what currently playing")
async def whatsplaying(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client
    await interaction.response.send_message(f"Currently Playing: {vc.track}")

bot.run("MTA4MzgwMjUxMDg3NzI3ODM2OQ.GS02YM.Rd5wmTjnfP5NHA7219OjvilmjmU09PdxiPwQUo")