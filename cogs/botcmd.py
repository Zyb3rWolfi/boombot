import nextcord
from nextcord.ext import commands
import wavelinkcord as wavelink

class BotCommands(commands.Cog):

    def __init__(self, bot):
        print("Bot Commands Loaded")
        self.bot = bot
    
    @nextcord.slash_command(guild_ids=[708632631901683723], name="about", description="About the Bot")
    async def about(self, interaction : nextcord.Interaction):

        em = nextcord.Embed(title="About The Bot") # IF QUEUE IS NOT EMPTY SEND AN EMBED
        em.add_field(name=f"BoomBot", value=f"A simple music bot for all your music needs.", inline=False)
        em.add_field(name=f"Creator", value="Zyb3rWolfi", inline=False)

        await interaction.response.send_message(embed=em)

def setup(bot : commands.Bot):
    print("Bot Commands Loaded")
    bot.add_cog(BotCommands(bot))