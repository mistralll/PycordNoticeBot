import sys
sys.path.append('../')
import disc.bot as bot

import discord
import disc.vc_notice.funcs as funcs
import disc.libs.voice_channel as vc
import disc.random_teaming.funcs as random_teaming

@bot.bot.event # 通話検知
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    op = funcs.detect_operation(before, after)
    if op == "start":
        bot.bot.dispatch("vc_start", member, after.channel)
    if op == "end":
        bot.bot.dispatch("vc_end", before.channel)
    if op == "many":
        bot.bot.dispatch("vc_many", member, after.channel)

@bot.bot.event # 通話開始
async def on_vc_start(mem: discord.Member, ch: discord.channel):
    bot.log(f"VC_Start: {ch.name} is started.")
    emb = discord.Embed(title=f"{ch.name} で通話が開始されました！", description=f"{mem.display_name}")
    chid = vc.detect_ch_id(bot.notice_channels, ch.id)
    await bot.bot.get_channel(int(chid)).send(embed=emb)

@bot.bot.event # 大人数参加
async def on_vc_many(mem: discord.Member, ch: discord.channel):
    bot.log(f"VC_Many: {mem.display_name} is join to {ch.name}.")
    emb = discord.Embed(title=f"{ch.name} に {vc.count_people(ch)}人目の参加者がきました！", description=f"来た人: {mem.display_name}")
    chid = vc.detect_ch_id(bot.notice_channels, ch.id)
    await bot.bot.get_channel(int(chid)).send(embed=emb)

@bot.bot.event # 通話終了
async def on_vc_end(ch: discord.channel):
    bot.log(f"VC_End: {ch.name} is ended.")
    emb = discord.Embed(title=f"{ch.name} の通話は終了しました")
    chid = vc.detect_ch_id(bot.notice_channels, ch.id)
    await bot.bot.get_channel(int(chid)).send(embed=emb)
    await random_teaming.delete_temp(ch, bot.temp_cat)

