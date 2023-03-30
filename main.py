import nextcord
from nextcord.ext import commands
from nextcord.shard import EventItem
import wavelinkcord as wavelink
import random
from wavelinkcord.ext import spotify

bot_version = "1.0.0"

intents = nextcord.Intents.all()
client = nextcord.Client()
bot = commands.Bot(command_prefix=".", intents=intents)

# All the cogs that will be loaded
cogs = [
    "cogs.events",
    "cogs.play",
    "cogs.queue",
    "cogs.bot",
        ]

# Just a list of songs to appear in the bot's status
songs = [
    "Without Me - Eminem",
    "Heathens - 21 Pilots",
    "Ride - 21 Pilots",
    "Free Bird - Lynyrd Skynyrd",
    "MOTTO - NF",
    "Right Now - Confetti",
]

if __name__ == "__main__":
    for cog in cogs:
        print(f"Loading {cog}")
        bot.load_extension(cog)

# When the bot is ready, it will create a task to connect to the LavaLink Host
@bot.event
async def on_ready():
    print("Bot Ready!")
    bot.loop.create_task(on_node())
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.listening, name=f"{songs[random.randint(0, 5)]}"))

# This function joins a LavaLink Host
async def on_node():
    sc = spotify.SpotifyClient(
            client_id='ae86a2b160874edf9dbb6b69995b74a8',
            client_secret='d470e67805824350b4c778554ed89a12'
        )
    node: wavelink.Node = wavelink.Node(uri='http://lavalink.clxud.pro:2333', password='youshallnotpass')
    await wavelink.NodePool.connect(client=bot, nodes=[node], spotify=sc)
    wavelink.Player.autoplay = True

bot.run("MTA4MzgwMjUxMDg3NzI3ODM2OQ.G91aF-.u88maMdv0hVL4vZhiRE9OSWeHaBrUu6QbZ6Ud4")