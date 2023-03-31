import nextcord
from nextcord.ext import commands
import wavelinkcord as wavelink
from wavelinkcord.ext import spotify

class playCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    # Plays a song from Youtube or Spotify
    # Spotify is played when the bot detects a spotify link since it beggins with "https://open.spotify.com/track/"
    @nextcord.slash_command(description="Play a song")
    async def play(self, interaction : nextcord.Interaction, search : str):

        try:
            destination = interaction.user.voice.channel

            if not interaction.guild.voice_client:

                vc: wavelink.Player = await destination.connect(cls=wavelink.Player)

            else:

                if (interaction.guild.voice_client.channel.id != destination.id):
                        
                        await interaction.guild.voice_client.move_to(destination)
                        
                vc: wavelink.Player = interaction.guild.voice_client  
            
            
            if "https://open.spotify.com/playlist" in search:
                print("Playlist Detected")
                async for track in spotify.SpotifyTrack.iterator(query=search):
                    await vc.queue.put_wait(track)
                    
                await vc.play(track)
                await interaction.response.send_message(f"Playlist Added To Queue")
                
            elif "https://open.spotify.com/track" in search:

                query = await spotify.SpotifyTrack.search(search)
                await interaction.response.send_message(f"Now Playing: {query.title}")
                
            else:
                
                query = await wavelink.YouTubeTrack.search(search, return_first=True)
                embed = nextcord.Embed(title=f"{query.title}", url=query.uri)
                embed.set_author(name="Added to the queue")
                embed.set_thumbnail(url=query.thumbnail)
                embed.add_field(name="Channel", value=vc.channel.name, inline=True)
                embed.add_field(name="Duration", value=round((query.duration / 1000) / 60, 2), inline=True)
                embed.add_field(name="Position in Queue", value=len(vc.queue) + 1, inline=False)
                
            if vc.queue.is_empty and not vc.is_playing():

                await vc.play(query)
                
                await interaction.response.send_message(embed=embed)
                
            else:
                await vc.queue.put_wait(query)
                await interaction.response.send_message(embed=embed)
                
        except:
            await interaction.response.send_message("Join a VC First!")

    @nextcord.slash_command(guild_ids=[708632631901683723])
    async def spotify(self, interaction : nextcord.Interaction, search : str):

        try:
            destination = interaction.user.voice.channel

            if not interaction.guild.voice_client:

                vc: wavelink.Player = await destination.connect(cls=wavelink.Player)
            elif interaction.guild.voice_client:

                vc: wavelink.Player = interaction.guild.voice_client 
        except:
            await interaction.response.send_message("Join a VC First!")

        async for track in spotify.SpotifyTrack.iterator(query=search):
            await vc.queue.put_wait(track)
        
        
        await vc.play(track)
    
    # Skips the current song by stopping it and then "on_wavelink_track_end" starts the next song
    # Wont skip the song if either the queue is empty or if loop is on
    @nextcord.slash_command(description="Skip the current song")
    async def skip(self, interaction : nextcord.Interaction):

        vc: wavelink.Player = interaction.guild.voice_client
        await vc.stop()
        if not vc.queue.is_empty:

            await vc.stop()
            await interaction.response.send_message("Song skipped!")
        
        elif vc.queue.loop == True:

            await interaction.response.send_message("Turn off looping to skip!")
        else:

            await interaction.response.send_message("Cant Skip! There is nothing in the Queue")
    
    # Disconnects the bot from the VC
    @nextcord.slash_command(description="Disconnects the bot from a VC")
    async def disconnect(self, interaction : nextcord.Interaction):

        vc: wavelink.Player = interaction.guild.voice_client
        await vc.disconnect()
        await interaction.response.send_message("Disconnected the Bot")

    # Pauses the current playing song
    @nextcord.slash_command(description="Pause a song")#
    async def pause(self, interaction : nextcord.Interaction):
        vc: wavelink.Player = interaction.guild.voice_client
        try:
            await vc.pause()
            await interaction.response.send_message("Paused the current song")
        except:
            await interaction.response.send_message("Song is already Pasued!")

    # Resumes the current song
    @nextcord.slash_command(description="Pause a song")
    async def resume(self, interaction : nextcord.Interaction):

        vc: wavelink.Player = interaction.guild.voice_client
        try:      
            await vc.resume()
            await interaction.response.send_message("Resumed the current song")
        except:
            await interaction.response.send_message("Song is already resumed!")

    # Shows what song is currently playing
    @nextcord.slash_command(description="Shows what currently playing")
    async def whatsplaying(self, interaction : nextcord.Interaction):

        vc: wavelink.Player = interaction.guild.voice_client

        try:        
            await interaction.response.send_message(f"Currently Playing: {vc.current.title}")
        except:
            await interaction.response.send_message("Nothing is currently playing")

    # Loops the current song
    @nextcord.slash_command(description="Loops a song")
    async def loop(self, interaction : nextcord.Interaction):
        
        vc: wavelink.Player = interaction.guild.voice_client
        if vc.queue.loop:
            vc.queue.loop = False
            print(vc.queue.loop)
            await interaction.response.send_message("Looping is turned off")
        else:
            vc.queue.loop = True
            print(vc.queue.loop)
            await interaction.response.send_message("Looping is turned on")

def setup(bot : commands.Bot):
    bot.add_cog(playCommands(bot))
