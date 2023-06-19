import nextcord
from nextcord.ext import commands
import wavelink as wavelink
from wavelink.ext import spotify
import sqlite3
from nextcord.ext import application_checks

database = sqlite3.connect('database.db')
cursor = database.cursor()

class djCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(description="A DJ command")
    @application_checks.has_permissions(manage_roles=True)
    async def dj(self, interaction):

        pass

    # First checks if dj mode is enabled, if it is then it checks if the user is a DJ if not it returns

    async def djCheck(self, interaction, event):

        query = "SELECT dj_id FROM dj WHERE guild_id = ?"
        djs = cursor.execute(query, (interaction.guild.id,)).fetchall()
        djCheck = "SELECT dj_mode FROM guilds WHERE guild_id = ?"
        djMode = cursor.execute(djCheck, (interaction.guild.id,)).fetchone()

        if djMode[0] == 0:
            await event()
            return
        else:
            for member in djs:
                if member[0] == interaction.user.id or djMode[0] == 0:
                    await event()
                    return
                
            await interaction.response.send_message("You are not a DJ")

    # Add a DJ to the database
    @dj.subcommand(description="Add a DJ")
    @application_checks.has_permissions(manage_roles=True)
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
    @application_checks.has_permissions(manage_roles=True)
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
    @application_checks.has_permissions(manage_roles=True)
    async def mode(self, interaction : nextcord.Interaction, option : bool  = nextcord.SlashOption(
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
    
    @dj.subcommand(description="List all DJs")
    async def list(self, interaction : nextcord.Interaction):

        query = "SELECT dj_id FROM dj WHERE guild_id = ?"
        djs = cursor.execute(query, (interaction.guild.id,)).fetchall()
        count = 0
        embed = nextcord.Embed(title="DJ List", description="List of all DJs", color=0x00ff00)
        for dj in djs:
            count += 1
            embed.add_field(name=f"`{count}`", value=f"<@{dj[0]}>, ")

        await interaction.response.send_message(embed=embed)

def setup(bot):
    bot.add_cog(djCommands(bot))