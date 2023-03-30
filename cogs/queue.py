import nextcord
from nextcord.ext import commands
import wavelinkcord as wavelink

class queueCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Creates a subcommand for the queue command
    @nextcord.slash_command()
    async def queue(self, interaction : nextcord.Interaction):

        pass
    
    # Shows the current queue by copying the queue and then adding each song to an embed
    @queue.subcommand(description="Shows the current Queue")
    async def list(self, interaction : nextcord.Interaction):
        vc: wavelink.Player = interaction.guild.voice_client
        if not vc.queue.is_empty:
            em = nextcord.Embed(title="Queue") 
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

    # Clears the queue using the clear method
    @queue.subcommand(description="Clears the Queue")
    async def clear(self, interaction : nextcord.Interaction):

        vc: wavelink.Player = interaction.guild.voice_client
        vc.queue.clear()
        await interaction.response.send_message("The Queue Has Been Cleared")
    
    # Removes a song from the queue
    @queue.subcommand(description="Removes a specific song from the queue")
    async def remove(self, interaction : nextcord.Interaction, position : int):

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


def setup(bot):
    bot.add_cog(queueCommands(bot))