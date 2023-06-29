import sys
sys.path.append('../')

import discord
import disc.bot as bot
import libs.env as env
import disc.random_teaming.funcs as funcs
import disc.libs.voice_channel as lib

@bot.bot.command(guildids=[env.GUILD_ID], description="ランダムでチーム分けします。")
async def random(ctx, vc:discord.VoiceChannel, num: int):
    # error handling
    if len(vc.members) < num:
        msg = "参加者の人数より多くは分割できません。"
        await ctx.respond(msg)
        return
    else:
        msg = f"{vc.name} を {num} 部屋にランダムに分けます。"
        await ctx.respond(msg)
    # Prepare Category
    cat = await funcs.get_or_create_category(ctx, bot.temp_category_name)
    bot.temp_cat = cat
    # Create voice channels
    channels = await funcs.create_temp_channels(ctx, vc.name, num, cat)
    # Set notice channel
    notice_ch = lib.detect_ch_id(bot.notice_channels, vc.id)
    for ch in channels:
        bot.notice_channels.append([str(ch.id), notice_ch])
    # Move people
    await funcs.move_random(vc, channels)
    bot.log(f"Random teaming: {vc.name}")