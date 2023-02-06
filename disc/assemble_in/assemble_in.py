import sys
sys.path.append('../')

import discord
import disc.bot as bot
import libs.env as env
import disc.random_teaming.funcs as rand

@bot.bot.slash_command(guildids=[env.GUILD_ID], description="指定のvcに集合させます。")
async def assemble_in(ctx, to:discord.VoiceChannel):
    await ctx.respond(f"{to.name}に集合させます。")
    for vc in bot.temp_cat.voice_channels:
        for mem in vc.members:
            await mem.move_to(to)
        rand.delete_temp(vc, bot.temp_cat)        

    bot.log(f"assemble_in to {to.name} is done.")

