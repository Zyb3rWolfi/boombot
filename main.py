import nextcord
from nextcord.ext import commands
from nextcord.shard import EventItem
import wavelinkcord as wavelink
import random
from wavelinkcord.ext import spotify
import sqlite3

database = sqlite3.connect('database.db')
cursor = database.cursor()
database.execute("CREATE TABLE IF NOT EXISTS dj (guild_id INTEGER, dj_id INTEGER)")
database.execute("CREATE TABLE IF NOT EXISTS guilds(guild_id INTEGER, dj_mode BOOLEAN, shuffle BOOLEAN)")

bot_version = "1.5.0"

intents = nextcord.Intents.all()
client = nextcord.Client()
bot = commands.Bot(command_prefix=".", intents=intents)

# All the cogs that will be loaded
extensions = [
    'cogs.botcmd',
    'cogs.events',
    'cogs.play',
    'cogs.queue',
    'cogs.dj',
        ]

if __name__ == "__main__":
    for ext in extensions:
            print(f"Loading {ext}")
            bot.load_extension(ext)

# Just a list of songs to appear in the bot's status
songs = [
    "Without Me - Eminem",
    "Heathens - 21 Pilots",
    "Ride - 21 Pilots",
    "Free Bird - Lynyrd Skynyrd",
    "MOTTO - NF",
    "Right Now - Confetti",
]

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


@bot.command()
async def test(ctx):
    await ctx.send("Test")



bot.run("")