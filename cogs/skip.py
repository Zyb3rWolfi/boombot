import nextcord
from nextcord.ext import commands
import wavelink as wavelink
from cogs.dj import djCommands as dj

class Buttons(nextcord.ui.View):

    def __init__(self, ctx):
        super().__init__()
        self.value = None
    
    @nextcord.ui.button(label = "Vote Skip", style = nextcord.ButtonStyle.gray)
    async def accept(self, button : nextcord.ui.Button, interaction : nextcord.Interaction):

        pass

class skipButtons(nextcord.ui.View):

    def __init__(self, ctx):
        super().__init__()
        self.value = 0

    
    @nextcord.ui.button(label = "Vote Skip", style = nextcord.ButtonStyle.gray)
    async def vote(self, button : nextcord.ui.Button, interaction : nextcord.Interaction):

        self.value += 1

        if self.value >= len(interaction.guild.voice_client.channel.members) - 1:
            await interaction.response.send_message("Vote Skip Passed!")
            vc: wavelink.Player = interaction.guild.voice_client
            await vc.stop()
            self.stop()

class skipCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Skips the current song by stopping it and then "on_wavelink_track_end" starts the next song
    # Wont skip the song if either the queue is empty or if loop is on
    @nextcord.slash_command(description="Skip the current song")
    async def skip(self, interaction : nextcord.Interaction):

        async def skip():
            listeners = len(interaction.guild.voice_client.channel.members) - 1

            if listeners == 1:
                vc: wavelink.Player = interaction.guild.voice_client
                await vc.stop()
                if not vc.queue.is_empty:

                    await vc.stop()
                    await interaction.response.send_message("Song skipped!")
                
                elif vc.queue.loop == True:

                    await interaction.response.send_message("Turn off looping to skip!")
                else:

                    await interaction.response.send_message("Cant Skip! There is nothing in the Queue")
            else:
                await interaction.response.send_message(f"Vote Skip Started! {listeners} votes needed to skip!", view=skipButtons(interaction))

        await dj.djCheck(self, interaction, skip)
    

def setup(bot : commands.Bot):
    bot.add_cog(skipCommands(bot))