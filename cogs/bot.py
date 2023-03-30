import nextcord
from nextcord.ext import commands
import wavelinkcord as wavelink
import main

class botCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(description="About the Bot")
    async def about(self, interaction : nextcord.Interaction):

        bot_version = main.bot_version

        em = nextcord.Embed(title="About The Bot") # IF QUEUE IS NOT EMPTY SEND AN EMBED
        em.add_field(name=f"BoomBot", value=f"A simple music bot for all your music needs.", inline=False)
        em.add_field(name=f"Version", value=f"{bot_version}", inline=False)
        em.add_field(name=f"Creator", value="Zyb3rWolfi", inline=False)

        await interaction.response.send_message(embed=em)

def setup(bot):
    bot.add_cog(botCommands(bot))