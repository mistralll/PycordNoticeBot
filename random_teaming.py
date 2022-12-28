import discord
import random

async def move_random(channel_move_from: discord.VoiceChannel, channels_move_to: list[discord.VoiceChannel]):
    # 第一引数のVoiceChannelに参加しているメンバーをランダムでmove_toのボイスチャンネルに均等に分配します。
    members = channel_move_from.members
    random.shuffle(members)
    for i, mem in enumerate(members):
        ch = channels_move_to[i % len(channels_move_to)]
        await mem.move_to(ch)

async def create_vc_in_category(ctx, vc_name: str, cat: discord.CategoryChannel):
    ch = await ctx.guild.create_voice_channel(vc_name, category=cat)
    return ch

async def get_category_by_name(ctx, name:str):
    cat = discord.utils.get(ctx.guild.categories, name=name)
    return cat

async def create_category(ctx, name: str):
    cat = await ctx.guild.create_category(name)
    return cat

async def get_or_create_category(ctx, name: str):
    cat = await get_category_by_name(ctx, name)
    if cat is None:
        cat = await create_category(ctx, name)
    return cat
