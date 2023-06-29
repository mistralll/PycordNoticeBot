import sys
sys.path.append('../')
import disc.bot as bot

import discord
import libs.env as env

@bot.bot.command(guild_ids=[env.GUILD_ID], description="指定のユーザーに援護ピンを立てます。") # 援護ピン
async def engo(ctx, user : discord.User):
    msg = f"{user.mention}を援護！"
    bot.log(f"Slash_Engo: {msg}")
    await ctx.respond(msg)