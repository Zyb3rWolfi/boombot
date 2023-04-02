import nextcord
from nextcord.ext import commands

# Embed when the play command is run
def playEmbed(query, vc):
    print("Embed Sent")
    embed = nextcord.Embed(title=f"{query.title}", url=query.uri)
    embed.set_author(name="Added to the queue")
    embed.set_thumbnail(url=query.thumbnail)
    embed.add_field(name="Channel", value=vc.channel.name, inline=True)
    embed.add_field(name="Duration", value=round((query.duration / 1000) / 60, 2), inline=True)
    embed.add_field(name="Position in Queue", value=len(vc.queue) + 1, inline=False)

    return embed

# embed when whatsplaying command is run
def whatsPlaying(vc):

    embed = nextcord.Embed(title=f"{vc.current.title}", url=vc.current.uri)
    embed.add_field(name="Channel", value=vc.channel.name, inline=True)
    embed.add_field(name="Duration", value=round((vc.current.duration / 1000) / 60, 2), inline=True)
    embed.set_author(name="Currently Playing")
    embed.set_thumbnail(url=vc.current.thumbnail)

    return embed

def whatsPlayingSpotify(song, vc):

    embed = nextcord.Embed(title=f"{song.title}")
    embed.add_field(name="Channel", value=vc.channel.name, inline=True)
    embed.add_field(name="Duration", value=round((vc.current.duration / 1000) / 60, 2), inline=True)
    embed.set_author(name="Currently Playing")

    return embed

# Help Command
def helpCommand():
    
    embed = nextcord.Embed(title="Help", description="List of commands")
    embed.add_field(name="`/play`", value="Plays a song from youtube or spotify", inline=False)
    embed.add_field(name="`/pause`", value="Pauses the current song", inline=False)
    embed.add_field(name="`/resume`", value="Resumes the current song", inline=False)
    embed.add_field(name="`/skip`", value="Skips the current song", inline=False)
    embed.add_field(name="`/disconnect`", value="Disconnects the bot", inline=False)
    embed.add_field(name="`/queue`", value="Shows the current queue", inline=False)
    embed.add_field(name="`/queue clear`", value="Clears the current queue", inline=False)
    embed.add_field(name="`/queue remove`", value="Removes a song from the queue", inline=False)
    embed.add_field(name="`/queue skipto`", value="Skips to a specific song in the queue", inline=False)
    embed.add_field(name="`/whatsplaying`", value="Shows the current song", inline=False)
    embed.add_field(name="`/help`", value="Shows this message", inline=False)
    embed.set_footer(text="Made by @Zyb3rWolfi#3614")

    return embed
