import nextcord
from nextcord.ext import commands
import wavelinkcord as wavelink
from wavelinkcord.ext import spotify
import cogs.embeds as embeds
import sqlite3

database = sqlite3.connect('database.db')
cursor = database.cursor()

class playCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    def getDjs(self, interaction):

        query = "SELECT dj_id FROM dj WHERE guild_id = ?"
        djs = cursor.execute(query, (interaction.guild.id,)).fetchall()

        return djs

    def getDjMode(self, interaction):

        djCheck = "SELECT dj_mode FROM guilds WHERE guild_id = ?"
        djMode = cursor.execute(djCheck, (interaction.guild.id,)).fetchone()

        return djMode

    # Plays a song from Youtube or Spotify
    # Spotify is played when the bot detects a spotify link since it beggins with "https://open.spotify.com/track/"
    @nextcord.slash_command(description="Play a song")
    async def play(self, interaction : nextcord.Interaction, search : str):

        djs = self.getDjs(interaction)
        djMode = self.getDjMode(interaction)
        print(djs, djMode)
        
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

        for member in djs:
             
            if member[0] == interaction.user.id or djMode[0] == 0:
                await play()
                return
            
        if djMode[0] == 0:
            await play()
            return
        else:
            await interaction.response.send_message("You are not a DJ!")

    
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

        getDjs = self.getDjs(interaction)
        djMode = self.getDjMode(interaction)

        for member in getDjs:
            if member[0] == interaction.user.id or djMode[0] == 0:
                await skip()
                return
        
        if djMode[0] == 0:
            await skip()
            return
        else:
            await interaction.response.send_message("You are not a DJ!")
    
    # Disconnects the bot from the VC
    @nextcord.slash_command(description="Disconnects the bot from a VC")
    async def disconnect(self, interaction : nextcord.Interaction):

        async def disconnect():
            vc: wavelink.Player = interaction.guild.voice_client
            await vc.disconnect()
            await interaction.response.send_message("Disconnected the Bot")
        
        getDjs = self.getDjs(interaction)
        djMode = self.getDjMode(interaction)

        for member in getDjs:
            if member[0] == interaction.user.id or djMode[0] == 0:
                await disconnect()
                return
        
        if djMode[0] == 0:
            await disconnect()
            return
        else:
            await interaction.response.send_message("You are not a DJ!")

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
        
        getDjs = self.getDjs(interaction)
        djMode = self.getDjMode(interaction)

        for member in getDjs:
            if member[0] == interaction.user.id or djMode[0] == 0:
                await pause()
                return
        
        if djMode[0] == 0:
            await pause()
            return

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

        getDjs = self.getDjs(interaction)
        djMode = self.getDjMode(interaction)

        for member in getDjs:
            if member[0] == interaction.user.id or djMode[0] == 0:
                await resume()
                return
        
        if djMode[0] == 0:
            await resume()
            return
        else:
            await interaction.response.send_message("You are not a DJ!")

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

        getDjs = self.getDjs(interaction)
        djMode = self.getDjMode(interaction)

        for member in getDjs:
            if member[0] == interaction.user.id or djMode[0] == 0:
                await loop()
                return
        
        if djMode[0] == 0:
            await loop()
            return
        else:
            await interaction.response.send_message("You are not a DJ!")
    
    @nextcord.slash_command(description="Replays the current song")
    async def replay(self, interaction : nextcord.Interaction):

        async def replay():
            vc: wavelink.Player = interaction.guild.voice_client
            await vc.play(vc.current)
            await interaction.response.send_message("Replaying the current song")
        
        getDjs = self.getDjs(interaction)
        djMode = self.getDjMode(interaction)

        for member in getDjs:
            if member[0] == interaction.user.id or djMode[0] == 0:
                await replay()
                return
        
        if djMode[0] == 0:
            await replay()
            return
        else:
            await interaction.response.send_message("You are not a DJ!")
        

def setup(bot : commands.Bot):
    bot.add_cog(playCommands(bot))
