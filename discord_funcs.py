# Prepare discord instance
import discord
import env
import log
import ping_pong
import vc_funcs
import db
import random_teaming

discord_intents = discord.Intents.all()
discord_intents.members = True

notice_channels = db.get_all_notice_channel_ids()
bot = discord.Bot(intents = discord_intents)

temp_category_name = "temporary"

@bot.event
async def on_ready():
    log.logger.info("Listening...")


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    res = ping_pong.make_res(message.content)
    if res != "":
        log.logger.info(f"PingPong: {res}")
        await message.channel.send(res)

@bot.event # 通話検知
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    op = vc_funcs.detect_operation(before, after)
    if op == "start":
        bot.dispatch("vc_start", member, after.channel)
    if op == "end":
        bot.dispatch("vc_end", before.channel)
    if op == "many":
        bot.dispatch("vc_many", member, after.channel)

@bot.event # 通話開始
async def on_vc_start(mem: discord.Member, ch: discord.channel):
    log.logger.info(f"VC_Start: {ch.name} is started.")
    emb = discord.Embed(title=f"{ch.name} で通話が開始されました！", description=f"{mem.display_name}")
    chid = vc_funcs.detect_ch_id(notice_channels, ch.id)
    await bot.get_channel(int(chid)).send(embed=emb)

@bot.event # 大人数参加
async def on_vc_many(mem: discord.Member, ch: discord.channel):
    log.logger.info(f"VC_Many: {mem.display_name} is join to {ch.name}.")
    emb = discord.Embed(title=f"{ch.name} に {vc_funcs.count_people(ch)}人目の参加者がきました！", description=f"来た人: {mem.display_name}")
    chid = vc_funcs.detect_ch_id(notice_channels, ch.id)
    await bot.get_channel(int(chid)).send(embed=emb)

@bot.event # 通話終了
async def on_vc_end(ch: discord.channel):
    log.logger.info(f"VC_End: {ch.name} is ended.")
    emb = discord.Embed(title=f"{ch.name} の通話は終了しました")
    chid = vc_funcs.detect_ch_id(notice_channels, ch.id)
    await bot.get_channel(int(chid)).send(embed=emb)
    
    # temporary channel だった場合削除する
    print(ch.category_id)


@bot.slash_command(guild_ids=[env.GUILD_ID], description="指定のユーザーに援護ピンを立てます。") # 援護ピン
async def engo(ctx, user : discord.User):
    msg = f"{user.mention}を援護！"
    log.logger.info(f"Slash_Engo: {msg}")
    await ctx.respond(msg)

@bot.slash_command(guildids=[env.GUILD_ID], description="通話開始通知を行うデフォルトのチャンネルを変更します。")
async def change_default_notice_channel(ctx, text_ch:discord.TextChannel):
    msg = f"デフォルトの通知先を{text_ch.name}に変更しました。"
    await ctx.respond(msg)
    db.change_or_add_notice_channel("default", str(text_ch.id))
    global notice_channels
    notice_channels = db.get_all_notice_channel_ids()
    log.logger.info(f"Slash_change_default_notice_ch: {text_ch.name}")
    

@bot.slash_command(guildids=[env.GUILD_ID], description="ボイスチャンネルの通知先を個別に設定します。")
async def change_notice_channel(ctx, voice_ch:discord.VoiceChannel, text_ch:discord.TextChannel):
    msg = f"{voice_ch.name}の通知先を{text_ch.name}に変更しました。"
    await ctx.respond(msg)
    db.change_or_add_notice_channel(str(voice_ch.id), str(text_ch.id))
    global notice_channels
    notice_channels = db.get_all_notice_channel_ids()
    log.logger.info(f"Slash_change_notice_ch: {text_ch.name} <- {voice_ch.name}")
    

@bot.slash_command(guildids=[env.GUILD_ID], description="ボイスチャンネルの通知先をデフォルトに戻します。")
async def change_notice_ch_to_default(ctx, voice_ch:discord.VoiceChannel):
    msg = f"{voice_ch.name}の通知先をデフォルトのチャンネルに変更しました。"
    await ctx.respond(msg)
    db.delete_db_row(str(voice_ch.id))
    global notice_channels
    notice_channels = db.get_all_notice_channel_ids()
    log.logger.info(f"Slash_change_notice_ch_to_default: {voice_ch.name}")

@bot.slash_command(guildids=[env.GUILD_ID], description="ランダムでチーム分けします。")
async def random(ctx, vc:discord.VoiceChannel, num: int):
    msg = f"移動中..."
    await ctx.respond(msg)
    ch_a = bot.get_channel(int(1057118636529168384))
    ch_b = bot.get_channel(int(1057119010812076032))
    await random_teaming.move_random(vc, [ch_a, ch_b])
    log.logger.info(f"Random teaming: {vc.name}")

@bot.slash_command(guildids=[env.GUILD_ID], description="dev - 一時的なボイスチャンネルを作ります。")
async def make_temp_vc(ctx, name:str):
    cat = await random_teaming.get_or_create_category(ctx, temp_category_name)
    ch  = await random_teaming.create_vc_in_category(ctx, name, cat)
    log.logger.info(f"create ch {ch.name} on {cat.name}")

bot.run(env.DISCORD_BOT_TOKEN)