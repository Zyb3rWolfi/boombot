async def on_node():
        node: wavelink.Node = wavelink.Node(uri='http://lavalink.clxud.pro:2333', password='youshallnotpass')
        await wavelink.NodePool.connect(client=bot, nodes=[node])

bot.loop.create_task(node_connect())

async def node_connect():
    await bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot=bot, host="node1.kartadharta.xyz", port=443, password="kdlavalink", https=True)

@bot.event
async def on_wavelink_node_ready(node: wavelink.Node):
    print(f"Node {node.identifier} Is Ready!")

# PLAY COMMAND
@bot.slash_command(guild_ids=[708632631901683723])

async def play(interaction : nextcord.Interaction, search : str, channel : nextcord.VoiceChannel):
        
        query = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        
        vc : wavelink.Player = await channel.connect(cls=wavelink.Player)

        await vc.play(query)

# SKIP COMMAND
@bot.slash_command(guild_ids=[708632631901683723])
async def skip(interaction : nextcord.Interaction):
     vc: wavelink.Player = interaction.guild.voice_client
     currentTrack = vc.queue.get()
     await vc.play(currentTrack)


@bot.slash_command(guild_ids=[708632631901683723])
async def pause(interaction : nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if vc.is_paused():
        await interaction.send("Already Paused!")
    else:
        await vc.pause()
        await interaction.send("Paused!")

@bot.slash_command(guild_ids=[708632631901683723])
async def resume(interaction : nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    if not vc.is_paused():
        await interaction.send("Already Resumed!")
    else:
        await vc.resume()
        await interaction.send("Resumed!")

@bot.slash_command(guild_ids=[])
async def queue(interaction : nextcord.Interaction):
    vc: wavelink.Player = interaction.guild.voice_client
    em = nextcord.Embed(title="Queue") 
    queue = vc.queue.copy()
    songs = []
    song_count = 0

    for song in queue:
        song_count += 1
        songs.append(song)
        em.add_field(name=f"[{song_count}] Duration {song.duration}", value=f"{song.title}", inline=False)

    await interaction.send(embed=em)

@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track: wavelink.Track, reason):
     ctx = player
     vc: player = ctx.guild.voice_client

     next_song = vc.queue.get()
     await vc.play(next_song)