import nextcord
from nextcord.ext import commands
import wavelinkcord as wavelink
from wavelinkcord.ext import spotify
import cogs.embeds as embeds
import sqlite3
import random
from cogs.dj import djCommands as dj

database = sqlite3.connect('database.db')
cursor = database.cursor()

# Add a way to load DJ commands and unload normal ones vice versa to improve overall performance of the Discord Bot
# since a the moment we have a lot of repetitve For loops!

class playCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    global shuffle_Toggle
    shuffle_Toggle = False

    # Plays a song from Youtube or Spotify
    # Spotify is played when the bot detects a spotify link since it beggins with "https://open.spotify.com/track/"
    @nextcord.slash_command(description="Play a song")
    async def play(self, interaction : nextcord.Interaction, search : str):
        
        async def play():
            try:
                destination = interaction.user.voice.channel

                if not interaction.guild.voice_client:

                    vc: wavelink.Player = await destination.connect(cls=wavelink.Player)

                else:

                    if (interaction.guild.voice_client.channel.id != destination.id):
                            Player = interaction.guild.voice_client  

                            await interaction.guild.voice_client.move_to(destination)
                            
                    vc: wavelink.Player = interaction.guild.voice_client
                if "https://open.spotify.com/playlist" in search:
                    print("Playlist Detected")
                    async for track in spotify.SpotifyTrack.iterator(query=search):
                        await vc.queue.put_wait(track)

                    if not vc.is_playing():
                        
                        await vc.play(track)
                    
                    await interaction.response.send_message(f"Playlist Added To Queue")
                    return
                    
                elif "https://open.spotify.com/track" in search:

                    query = await spotify.SpotifyTrack.search(search)
                    await interaction.response.send_message(f"Now Playing: {query.title}")
                    
                else:
                    
                    query = await wavelink.YouTubeTrack.search(search, return_first=True)
                    
                    
                if vc.queue.is_empty and not vc.is_playing():

                    await vc.play(query)
                    embed = embeds.playEmbed(query, vc)
                    await interaction.response.send_message(embed=embed)
                    
                else:
                    await vc.queue.put_wait(query)
                    embed = embeds.playEmbed(query, vc)
                    await interaction.response.send_message(embed=embed)
                    
            except:
                await interaction.response.send_message("Join a VC First!")

        await dj.djCheck(self, interaction, play)

    
    # Skips the current song by stopping it and then "on_wavelink_track_end" starts the next song
    # Wont skip the song if either the queue is empty or if loop is on
    @nextcord.slash_command(description="Skip the current song")
    async def skip(self, interaction : nextcord.Interaction):

        async def skip():
            vc: wavelink.Player = interaction.guild.voice_client
            await vc.stop()
            if not vc.queue.is_empty:

                await vc.stop()
                await interaction.response.send_message("Song skipped!")
            
            elif vc.queue.loop == True:

                await interaction.response.send_message("Turn off looping to skip!")
            else:

                await interaction.response.send_message("Cant Skip! There is nothing in the Queue")

        await dj.djCheck(self, interaction, skip)
    
    # Disconnects the bot from the VC
    @nextcord.slash_command(description="Disconnects the bot from a VC")
    async def disconnect(self, interaction : nextcord.Interaction):

        async def disconnect():
            vc: wavelink.Player = interaction.guild.voice_client
            await vc.disconnect()
            await interaction.response.send_message("Disconnected the Bot")

        await dj.djCheck(self, interaction, disconnect)

    # Pauses the current playing song
    @nextcord.slash_command(description="Pause a song")#
    async def pause(self, interaction : nextcord.Interaction):

        async def pause():

            vc: wavelink.Player = interaction.guild.voice_client
            try:
                await vc.pause()
                await interaction.response.send_message("Paused the current song")
            except:
                await interaction.response.send_message("Song is already Pasued!")
        
        await dj.djCheck(self, interaction, pause)

    # Resumes the current song
    @nextcord.slash_command(description="Pause a song")
    async def resume(self, interaction : nextcord.Interaction):

        async def resume():
            vc: wavelink.Player = interaction.guild.voice_client
            try:      
                await vc.resume()
                await interaction.response.send_message("Resumed the current song")
            except:
                await interaction.response.send_message("Song is already resumed!")

        await dj.djCheck(self, interaction, resume)

    # Shows what song is currently playing
    @nextcord.slash_command(description="Shows what currently playing")
    async def whatsplaying(self, interaction : nextcord.Interaction):

        vc: wavelink.Player = interaction.guild.voice_client
        embed = embeds.whatsPlaying(vc)

        try:        
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message("Nothing is currently playing")

    # Loops the current song
    @nextcord.slash_command(description="Loops a song")
    async def loop(self, interaction : nextcord.Interaction):
        
        async def loop():

            vc: wavelink.Player = interaction.guild.voice_client
            if vc.queue.loop:
                vc.queue.loop = False
                print(vc.queue.loop)
                await interaction.response.send_message("Looping is turned off")
            else:
                vc.queue.loop = True
                print(vc.queue.loop)
                await interaction.response.send_message("Looping is turned on")

        await dj.djCheck(self, interaction, loop)
    
    @nextcord.slash_command(description="Replays the current song")
    async def replay(self, interaction : nextcord.Interaction):

        async def replay():
            vc: wavelink.Player = interaction.guild.voice_client
            await vc.play(vc.current)
            await interaction.response.send_message("Replaying the current song")

        await dj.djCheck(self, interaction, replay)
    
    @nextcord.slash_command(description="Shuffles the songs in the queue")
    async def shuffle(self, interaction : nextcord.Interaction):

        vc : wavelink.Player = interaction.guild.voice_client

        query = "SELECT SHUFFLE FROM guilds WHERE guild_id = ?"
        shuffle_status = cursor.execute(query, (interaction.guild.id,)).fetchone()

        async def shuffle():
            if shuffle_status[0] == 0:
                await interaction.response.send_message("Shuffling the queue")
                cursor.execute("UPDATE guilds SET shuffle = ? WHERE guild_id = ?", (True, interaction.guild.id,))
                database.commit()
                
            else:
                await interaction.response.send_message("Unshuffling the queue")
                cursor.execute("UPDATE guilds SET shuffle = ? WHERE guild_id = ?", (False, interaction.guild.id,))
                database.commit()
    
        
        await dj.djCheck(self, interaction, shuffle)
        

def setup(bot : commands.Bot):
    bot.add_cog(playCommands(bot))
