import nextcord
from nextcord.ext import commands
import wavelinkcord as wavelink
import cogs.embeds as embeds
import sqlite3

database = sqlite3.connect('database.db')
cursor = database.cursor()

# This is mainly utility commands for the bot like checking the latency, amount of servers, etc.

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
    
    @nextcord.slash_command(name="help", description="Display the list of commands")
    async def help(self, interaction : nextcord.Interaction):

        embed = embeds.helpCommand()
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="amount", description="Check the amount of servers the bot is in")
    async def amount(self, interaction : nextcord.Interaction):

        await interaction.response.send_message(f"I am in {len(self.bot.guilds)} servers")
    
    @nextcord.slash_command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction : nextcord.Interaction):
            
            await interaction.response.send_message(f"Pong! {round(self.bot.latency * 1000)}ms")
    
    @nextcord.slash_command(name="update", description="Updates Database", guild_ids=[708632631901683723])
    async def update(self, interaction : nextcord.Interaction):

        query = "SELECT * FROM guilds WHERE guild_id = ?"
        guilds = self.bot.guilds

        if cursor.execute(query, (interaction.guild.id,)).fetchone() == None:
             
            query = "INSERT INTO guilds VALUES (?,?,?)"
            cursor.execute(query, (interaction.guild.id, 0, 0))
        
        database.commit()
        await interaction.response.send_message("Database Updated")
    

def setup(bot : commands.Bot):
    print("Bot Commands Loaded")
    bot.add_cog(BotCommands(bot))