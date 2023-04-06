import nextcord
from nextcord.ext import commands
import sqlite3

database = sqlite3.connect('database.db')
cursor = database.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS messages(message_content STRING, message_id INT)")

class db(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command()
    async def write(self, interaction : nextcord.Interaction, message : str):

        query = "INSERT INTO messages VALUES (?, ?)"
        cursor.execute(query, (message, interaction.id))
        database.commit()

        await interaction.response.send_message("Message written to database")

    
    @nextcord.slash_command()
    async def delete(self, interaction : nextcord.Interaction, message : str):

        query = "DELETE FROM messages WHERE message_content = ?"
        cursor.execute(query, (message,))
        database.commit()

        await interaction.response.send_message("Message deleted from database")
    
    @nextcord.slash_command()
    async def read(self, interaction : nextcord.Interaction):

        query = "SELECT * FROM messages"
        data = cursor.execute(query).fetchall()

        for message in data:

            await interaction.send(f"Message: {message[0]}")
        
    @nextcord.slash_command()
    async def append(self, interaction : nextcord.Interaction, message : str, new_message : str):

        query = "UPDATE messages SET message_content = ? WHERE message_content = ?"
        cursor.execute(query, (new_message, message))
        database.commit()

        await interaction.response.send_message("Message updated in database")


def setup(bot):
    bot.add_cog(db(bot))