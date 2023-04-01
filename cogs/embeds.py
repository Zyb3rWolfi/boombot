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