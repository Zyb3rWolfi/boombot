import nextcord
from nextcord.ext import commands
import wavelink as wavelinkcord

class filterCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(description="A filter command")
    async def filter(self, interaction):
        pass

    @filter.subcommand(description="Set a filter for the bot")
    async def set(self, interaction, filters : int  = nextcord.SlashOption(
        name="filters", 
        choices={"Karaoke": 1, "Tremolo":2}
        )
        ):

        vc : wavelinkcord.Player = interaction.guild.voice_client
        
        if filters == 1:
            print("Karaoke")
            await interaction.response.send_message("Filter set to Karaoke")
            vc.set_filter(wavelinkcord.Filter.karaoke)
            
        elif filters == 2:

            await interaction.response.send_message("Filter set to Tremolo")

def setup(bot):
    bot.add_cog(filterCommands(bot))