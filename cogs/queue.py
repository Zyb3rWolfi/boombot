import nextcord
from nextcord.ext import commands
import wavelink as wavelinkcord
import cogs.embeds as embeds
from wavelink.ext import spotify
from cogs.dj import djCommands as dj


class queueCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Creates a subcommand for the queue command
    @nextcord.slash_command()
    async def queue(self, interaction : nextcord.Interaction):

        pass
    
    # Shows the current queue by copying the queue and then adding each song to an embed
    @queue.subcommand(description="Shows the current Queue")
    async def show(self, interaction : nextcord.Interaction):
        vc: wavelinkcord.Player = interaction.guild.voice_client
        if not vc.queue.is_empty:
            em = nextcord.Embed(title="Queue") 
            em.add_field(name=f"Now Playing", value=f"{vc.current.title}", inline=False)
            queue = vc.queue.copy()
            songs = []
            song_count = 0
            for song in queue:
                song_count += 1
                songs.append(song)
                if song_count == 1:
                    em.add_field(name=f"Up Next", value=f"`[{song_count}]` {song.title}", inline=False)
                
                else:

                    em.add_field(name="", value=f"`[{song_count}]` {song.title} [{round((song.duration / 1000) / 60, 2)}]", inline=False)

            await interaction.response.send_message(embed=em)
        else:
            await interaction.response.send_message("Queue is empty!")

    # Clears the queue using the clear method
    @queue.subcommand(description="Clears the Queue")
    async def clear(self, interaction : nextcord.Interaction):
        async def clear():
            vc: wavelinkcord.Player = interaction.guild.voice_client
            vc.queue.clear()
            await interaction.response.send_message("The Queue Has Been Cleared")
        
        await dj.djCheck(self, interaction, clear)
    
    # Removes a song from the queue
    @queue.subcommand(description="Removes a specific song from the queue")
    async def remove(self,interaction : nextcord.Interaction, song : str):

        async def remove():

            vc: wavelinkcord.Player = interaction.guild.voice_client

            #This bit of code copys the queue object from the vc object then converts it to a list and removes the song from the list
            queue = vc.queue.copy()
            queue = list(queue)

            decoded = spotify.decode_url(song)
            if not decoded or decoded['type'] is not spotify.SpotifySearchType.track:
                query = await wavelinkcord.YouTubeTrack.search(song, return_first=True)
            else:
                query = await spotify.SpotifyTrack.search(song)

            try:
                queue.remove(query)
                await interaction.response.send_message(f"Sucsessfully removed {query.title} {query.uri}!")

            except:
                await interaction.response.send_message("Song not found in queue!")

            vc.queue.clear()

            # After clearing the queue, we loop through the queue and assign the songs to the player queue
            for song in queue:

                await vc.queue.put_wait(song)
        
        await dj.djCheck(self, interaction, remove)

    
    # Skips to a specific song in the queue
    @queue.subcommand(description="Removes a specific song from the queue")
    async def skipto(self, interaction : nextcord.Interaction, song_name : str):

        async def skipto():
            vc: wavelinkcord.Player = interaction.guild.voice_client

            decoded = spotify.decode_url(song_name)
            # This checks if the song is a spotify song, if no then searches on youtube
            if not decoded or decoded['type'] is not spotify.SpotifySearchType.track:

                query: list[wavelinkcord.YouTubeMusicTrack] = await wavelinkcord.YouTubeMusicTrack.search(song_name)
                query: wavelinkcord.YouTubeTrack = query[0]
                embed = embeds.playEmbed(query, vc)
            # If it is a spotify track then it searches on spotify
            else:
                query: list[spotify.SpotifyTrack] = await spotify.SpotifyTrack(song_name)
                query: spotify.SpotifyTrack = query[0]
                embed = embeds.whatsPlayingSpotify(query, vc)

            # Copies the queue to a list
            queue = vc.queue.copy()
            queue = list(queue)

            # Iterates through the queue until it finds the song needed
            for song in queue:
                if song.uri == query.uri:
                    await vc.play(song)
                    queue.remove(song)
                    await interaction.response.send_message(embed=embed)
                    break
            
            # Clears the track queue and adds the songs back to the queue
            vc.queue.clear()

            for song in queue:
                await vc.queue.put_wait(song)
        
        # Checks if the user is a dj
        await dj.djCheck(self, interaction, skipto)
    



def setup(bot : commands.Bot):
    bot.add_cog(queueCommands(bot))
