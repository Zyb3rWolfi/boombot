import nextcord
from nextcord.ext import commands
import wavelinkcord as wavelink
from wavelinkcord.ext import spotify
import sqlite3

database = sqlite3.connect('database.db')
cursor = database.cursor()

class djCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="A DJ command")
    async def dj(self, interaction):

        pass

    # Add a DJ to the database
    @dj.subcommand(description="Add a DJ")
    async def add(self, interaction : nextcord.Interaction, member : nextcord.Member):

        checkQuery = "SELECT dj_id FROM dj WHERE guild_id = ? AND dj_id = ?"

        if cursor.execute(checkQuery, (interaction.guild.id, member.id)).fetchone():
            await interaction.response.send_message(f"{member.mention} is already a DJ")
            return
        else:
            query = "INSERT INTO dj VALUES (?, ?)"
            cursor.execute(query, (interaction.guild.id, member.id))
            database.commit()
            await interaction.response.send_message(f"{member.mention} is now a DJ")
    
    # Remove a DJ from the database
    @dj.subcommand(description="Remove a DJ")
    async def remove(self, interaction : nextcord.Interaction, member : nextcord.Member):
            
            checkQuery = "SELECT dj_id FROM dj WHERE guild_id = ? AND dj_id = ?"

            if not cursor.execute(checkQuery, (interaction.guild.id, member.id)).fetchone():
                await interaction.response.send_message(f"{member.mention} is not a DJ")
                return
            else:
                query = "DELETE FROM dj WHERE guild_id = ? AND dj_id = ?"
                cursor.execute(query, (interaction.guild.id, member.id))
                database.commit()
                await interaction.response.send_message(f"{member.mention} is no longer a DJ")
    
    # Toggle DJ mode on or off via database
    @dj.subcommand(description="Toggle DJ mode")
    async def toggle(self, interaction : nextcord.Interaction, option : bool  = nextcord.SlashOption(
        name="option", 
        choices={"On": 1, "Off":2}
        )
        ):

        query = "UPDATE guilds SET dj_mode = ? WHERE guild_id = ?"
        cursor.execute(query, (option, interaction.guild.id))
        database.commit()

        if option == 1:
            await interaction.response.send_message("DJ mode is now on")
        else:
            await interaction.response.send_message("DJ mode is now off")

def setup(bot):
    bot.add_cog(djCommands(bot))