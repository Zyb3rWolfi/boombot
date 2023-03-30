import nextcord
from nextcord.ext import commands
import wavelinkcord as wavelink

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # Listens for a song to end and if the queue is empty it will disconnect the bot
    # Of loop is on it will loop the song
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, i):
        vc: wavelink.Player = i.player
        
        if vc.queue.loop == True:

            await vc.play(i.track)

        elif vc.queue.is_empty:

            await vc.disconnect()

def setup(bot):
    bot.add_cog(Events(bot))