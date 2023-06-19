import nextcord
from nextcord.ext import commands
import wavelink as wavelinkcord
from wavelink.ext import spotify
import cogs.embeds as embeds
import sqlite3
from cogs.dj import djCommands as dj

database = sqlite3.connect('database.db')
cursor = database.cursor()

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

                    vc: wavelinkcord.Player = await destination.connect(cls=wavelinkcord.Player)

                else:

                    if (interaction.guild.voice_client.channel.id != destination.id):
                            Player = interaction.guild.voice_client  

                            await interaction.guild.voice_client.move_to(destination)
                            
                    vc: wavelinkcord.Player = interaction.guild.voice_client
                if "https://open.spotify.com/playlist" in search or "https://open.spotify.com/album" in search:
                    print("Playlist Detected")
                    async for track in spotify.SpotifyTrack.iterator(query=search):
                        await vc.queue.put_wait(track)
                        print("Added to queue")

                    if not vc.is_playing():
                        
                        await vc.play(track)
                    
                    await interaction.response.send_message(f"Playlist Added To Queue")
                    return
                    
                elif "https://open.spotify.com/track" in search:
                    query: list[spotify.SpotifyTrack] = await spotify.SpotifyTrack.search(search)
                    query: spotify.SpotifyTrack = query[0]

                    await interaction.response.send_message(f"Now Playing: {query.title}")
                    
                else:
                    if not "https://www.youtube.com/playlist" in search:

                        query: list[wavelinkcord.YouTubeMusicTrack] = await wavelinkcord.YouTubeMusicTrack.search(search)
                        query: wavelinkcord.GenericTrack = query[0]

                    else:
                        print("youtube playlist")
                        playlist: list[wavelinkcord.YouTubePlaylist] = await wavelinkcord.YouTubePlaylist.search(search)
                        
                        tracks = playlist.tracks
                        for i in tracks:
                            
                            query : wavelinkcord.GenericTrack = i
                            await vc.queue.put_wait(query)

                            if not vc.is_playing():
                                await vc.play(query)
                            
                        await interaction.response.send_message(f"Playlist Added To Queue")


                        #for track in playlist.tracks:
                            #await vc.queue.put_wait(track)
                        
                        #print("Added to queue")
                    
                    
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
    
    # Disconnects the bot from the VC
    @nextcord.slash_command(description="Disconnects the bot from a VC")
    async def disconnect(self, interaction : nextcord.Interaction):

        async def disconnect():
            vc: wavelinkcord.Player = interaction.guild.voice_client
            await vc.disconnect()
            await interaction.response.send_message("Disconnected the Bot")

        await dj.djCheck(self, interaction, disconnect)

    # Pauses the current playing song
    @nextcord.slash_command(description="Pause a song")#
    async def pause(self, interaction : nextcord.Interaction):

        async def pause():

            vc: wavelinkcord.Player = interaction.guild.voice_client
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
            vc: wavelinkcord.Player = interaction.guild.voice_client
            try:      
                await vc.resume()
                await interaction.response.send_message("Resumed the current song")
            except:
                await interaction.response.send_message("Song is already resumed!")

        await dj.djCheck(self, interaction, resume)

    # Shows what song is currently playing
    @nextcord.slash_command(description="Shows what currently playing")
    async def whatsplaying(self, interaction : nextcord.Interaction):

        vc: wavelinkcord.Player = interaction.guild.voice_client
        embed = embeds.whatsPlaying(vc)

        try:        
            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message("Nothing is currently playing")

    # Loops the current song
    @nextcord.slash_command(description="Loops a song")
    async def loop(self, interaction : nextcord.Interaction):
        
        async def loop():

            vc: wavelinkcord.Player = interaction.guild.voice_client
            if vc.queue.loop:
                vc.queue.loop = False
                print(vc.queue.loop)
                await interaction.response.send_message("Looping is turned off")
            else:
                vc.queue.loop = True
                print(vc.queue.loop)
                await interaction.response.send_message("Looping is turned on")

        await dj.djCheck(self, interaction, loop)
    
    @nextcord.slash_command(description="Loops the queue")
    async def queue_loop(self, interaction : nextcord.Interaction):

        vc : wavelinkcord.Player = interaction.guild.voice_client
        if vc.queue.loop_all:

            vc.queue.loop_all = False
            await interaction.response.send_message("Queue looping is turned off")
        
        else:
                
            vc.queue.loop_all = True
            await interaction.response.send_message("Queue looping is turned on")
    
    @nextcord.slash_command(description="Replays the current song")
    async def replay(self, interaction : nextcord.Interaction):

        async def replay():
            vc: wavelinkcord.Player = interaction.guild.voice_client
            await vc.play(vc.current)
            await interaction.response.send_message("Replaying the current song")

        await dj.djCheck(self, interaction, replay)
    
    @nextcord.slash_command(description="Shuffles the songs in the queue")
    async def shuffle(self, interaction : nextcord.Interaction):

        vc : wavelinkcord.Player = interaction.guild.voice_client

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

    @nextcord.slash_command(description="Seeks a song in seconds")
    async def seek(self, interaction : nextcord.Interaction, seconds : int):

        vc: wavelinkcord.Player = interaction.guild.voice_client
        await vc.seek(seconds * 1000)
        await interaction.response.send_message(f"Seeked to {seconds} seconds")
    
    @nextcord.slash_command(description="Rewinds a song in seconds")
    async def rewind(self, interaction : nextcord.Interaction, seconds : int):
            
            vc: wavelinkcord.Player = interaction.guild.voice_client
            await vc.seek(vc.position - (seconds * 1000))
            await interaction.response.send_message(f"Rewinded {seconds} seconds")

def setup(bot : commands.Bot):
    bot.add_cog(playCommands(bot))
