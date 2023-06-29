import sys
sys.path.append('../')

import discord
import disc.bot as bot
import libs.env as env

@bot.bot.command(guildids=[env.GUILD_ID], description="ボイスチャンネルに参加している全員を移動させます。")
async def move_all(ctx, fm:discord.VoiceChannel, to:discord.VoiceChannel):
    msg = f"{fm.name} の参加者を {to.name} に移動させます。"
    await ctx.respond(msg)
    members = fm.members
    for mem in members:
        await mem.move_to(to)
    bot.log(f"move_all: {fm.name} to {to.name}")