import discord
import random

async def move_random(channel_move_from: discord.VoiceChannel, channels_move_to: list[discord.VoiceChannel]):
    # 第一引数のVoiceChannelに参加しているメンバーをランダムでmove_toのボイスチャンネルに均等に分配します。
    members = channel_move_from.members
    random.shuffle(members)
    print("check")
    for i, mem in enumerate(members):
        ch = channels_move_to[i % len(channels_move_to)]
        print(f"{mem.name} -> {ch.name}")
        await mem.move_to(ch)