import nextcord
from nextcord.ext import commands
from nextcord.shard import EventItem
import wavelinkcord as wavelink
import random

bot_version = "0.0.1"

intents = nextcord.Intents.all()
client = nextcord.Client()
bot = commands.Bot(command_prefix=".", intents=intents)

songs = [
    "Without Me - Eminem",
    "Heathens - 21 Pilots",
    "Ride - 21 Pilots",
    "Free Bird - Lynyrd Skynyrd",
    "MOTTO - NF",
    "Right Now - Confetti",
]

@bot.event
async def on_ready():
    print("Bot Ready!")
    bot.loop.create_task(on_node())
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=f"{songs[random.randint(0, 5)]}"))

# This function joins a LavaLink Host
async def on_node():
    node: wavelink.Node = wavelink.Node(uri='http://lavalink.clxud.pro:2333', password='youshallnotpass')
    await wavelink.NodePool.connect(client=bot, nodes=[node])
    wavelink.Player.autoplay = True

@bot.slash_command(guild_ids=[708632631901683723], description="About the Bot")
async def about(interaction : nextcord.Interaction):

    em = nextcord.Embed(title="About The Bot") # IF QUEUE IS NOT EMPTY SEND AN EMBED
    em.add_field(name=f"BoomBot", value=f"A simple music bot for all your music needs.", inline=False)
    em.add_field(name=f"Version", value=f"{bot_version}", inline=False)
    em.add_field(name=f"Creator", value="Zyb3rWolfi", inline=False)

    await interaction.response.send_message(embed=em)

@bot.event
async def on_wavelink_track_start(self):

    vc: wavelink.Player = self.player

@bot.event
async def on_wavelink_track_end(self):

    vc: wavelink.Player = self.player
    
    if vc.queue.loop == True:

        await vc.play(self.track)

    elif vc.queue.is_empty:

        await vc.disconnect()

# Searches a song on Youtube and plays it through the VC
@bot.slash_command(description="Search For a Song")
async def play(interaction : nextcord.Interaction, search : str):

    query = await wavelink.YouTubeTrack.search(search, return_first=True)
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
@bot.slash_command(description="Skip the current song")
async def skip(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client
    await vc.stop()
    if not vc.queue.is_empty:

        await vc.stop()
        await interaction.response.send_message("Song skipped!")
    
    elif vc.queue.loop == True:

        await interaction.response.send_message("Turn off looping to skip!")
    else:

        await interaction.response.send_message("Cant Skip! There is nothing in the Queue")

# Shows the current queue in an embed for the user
@bot.slash_command()
async def queue(interaction : nextcord.Interaction):

    pass

@queue.subcommand(description="Shows the current Queue")
async def list(interaction : nextcord.Interaction):
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

@queue.subcommand(description="Clears the Queue")
async def clear(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client
    vc.queue.clear()
    await interaction.response.send_message("The Queue Has Been Cleared")

# Disconnects the user from the channel
@bot.slash_command(description="Disconnects the bot from a VC")
async def disconnect(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client
    await vc.disconnect()
    await interaction.response.send_message("Disconnected the Bot")

# Pauses the current song
@bot.slash_command(description="Pause a song")#
async def pause(interaction : nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    try:
        await vc.pause()
        await interaction.response.send_message("Paused the current song")
    except:
        await interaction.response.send_message("Song is already Pasued!")

# Resumes the current song
@bot.slash_command(description="Pause a song")
async def resume(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client
    try:      
        await vc.resume()
        await interaction.response.send_message("Resumed the current song")
    except:
        await interaction.response.send_message("Song is already resumed!")

# Shows what song is currently playing
@bot.slash_command(description="Shows what currently playing")
async def whatsplaying(interaction : nextcord.Interaction):

    vc: wavelink.Player = interaction.guild.voice_client
    await interaction.response.send_message(f"Currently Playing: {vc.current.title}")

@bot.slash_command(description="Loops a song")
async def loop(interaction : nextcord.Interaction):
    
    vc: wavelink.Player = interaction.guild.voice_client
    if vc.queue.loop:
        vc.queue.loop = False
        print(vc.queue.loop)
        await interaction.response.send_message("Looping is turned off")
    else:
        vc.queue.loop = True
        print(vc.queue.loop)
        await interaction.response.send_message("Looping is turned on")

# Removes a song from the queue
@bot.slash_command(description="Removes a specific song from the queue")
async def remove(interaction : nextcord.Interaction, position : int):

    vc: wavelink.Player = interaction.guild.voice_client
    
    queue = vc.queue.copy()
    new_queue = []

    # Loops through the queue and only adding songs which wasnt selected by the user
    for song in queue:
        
        if (vc.queue[position - 1] != song):

            new_queue.append(song)
    
    vc.queue.clear()

    # After clearing the queue, we loop through the new queue and assign the songs to the player queue
    for song in new_queue:

        await vc.queue.put_wait(song)

@bot.slash_command(description="Searches a Youtube Playlist")
async def playlist(interaction : nextcord.Interaction, search : str):

    query = await wavelink.YouTubePlaylist.search(search, return_first=True)
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

bot.run("MTA4MzgwMjUxMDg3NzI3ODM2OQ.GS02YM.Rd5wmTjnfP5NHA7219OjvilmjmU09PdxiPwQUo")