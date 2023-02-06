import sys
sys.path.append('../')
import disc.bot as bot

import discord
import disc.libs.voice_channel as vc
import disc.random_teaming.funcs as random_teaming

def detect_operation(bf:discord.VoiceState, af:discord.VoiceState):
    # voice_stateの変化から通話の開始・終了・大人数の参加を検出します。
    bf_cnt = vc.count_people(bf.channel)
    af_cnt = vc.count_people(af.channel)

    is_dif_ch = True
    if bf_cnt != -1 and af_cnt != -1:
        is_dif_ch = bf.channel.id is af.channel.id

    if af_cnt != -1:
        if bf_cnt == -1 and af_cnt == 1:
            return "start"
        if af_cnt == 1 and not(is_dif_ch):
            return "start"
        if af_cnt > 3 and is_dif_ch and bf_cnt < af_cnt:
            return "many"
    if bf_cnt == 0:
        return "end"
    return -1

@bot.bot.event # 通話検知
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    op = detect_operation(before, after)
    if op == "start":
        await on_vc_start(member, after.channel)
    if op == "end":
        await on_vc_end(before.channel)
    if op == "many":
        await on_vc_many(member, after.channel)

# 通話開始
async def on_vc_start(mem: discord.Member, ch: discord.channel):
    bot.log(f"VC_Start: {ch.name} is started.")

    # If channel is temporary, then not notice its start.
    if random_teaming.is_temp_ch(ch, bot.temp_cat):
        bot.log(f"VC_Start: The channel is in temporary category.")
        return
    
    emb = discord.Embed(title=f"{ch.name} で通話が開始されました！", description=f"{mem.display_name}")
    chid = vc.detect_ch_id(bot.notice_channels, ch.id)
    await bot.bot.get_channel(int(chid)).send(embed=emb)


# 通話終了
async def on_vc_end(ch: discord.channel):
    bot.log(f"VC_End: {ch.name} is ended.")
    if random_teaming.is_temp_ch(ch, bot.temp_cat):
        # If the channel dose not belong to temporary category, call delete_function.
        await random_teaming.delete_temp(ch, bot.temp_cat)
    else:
        # If the channel dose not belong to temporary category, send message.
        emb = discord.Embed(title=f"{ch.name} の通話は終了しました")
        chid = vc.detect_ch_id(bot.notice_channels, ch.id)
        await bot.bot.get_channel(int(chid)).send(embed=emb) 

# 大人数の参加
async def on_vc_many(mem: discord.Member, ch: discord.channel):
    bot.log(f"VC_Many: {mem.display_name} is join to {ch.name}.")

    if random_teaming.is_temp_ch(ch, bot.temp_cat):
        # If the channel does not belong to temporary category, no message is sent.
        return

    emb = discord.Embed(title=f"{ch.name} に {vc.count_people(ch)}人目の参加者がきました！", description=f"来た人: {mem.display_name}")
    chid = vc.detect_ch_id(bot.notice_channels, ch.id)
    await bot.bot.get_channel(int(chid)).send(embed=emb)