import init
import ping_pong
import vc_funcs

# Prepare discord instance
import discord
bot = discord.Bot(intents = init.intents)

# Prepare env variable
import os
from dotenv import load_dotenv
load_dotenv()
DISCORD_BOT_TOKEN = os.environ['APP_BOT_TOKEN']
DISCORD_CLIENT_ID = os.environ['CLIENT_ID']
GUILD_ID = int(os.environ['GUILD_ID'])

# Prepare logger
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    res = ping_pong.make_res(message.content)
    if res != "":
        logger.info(f"PingPong: {res}")
        await message.channel.send(res)
    
@bot.event
async def on_ready():
    logger.info("Listening...")

@bot.event # 通話検知
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    op = vc_funcs.detect_operation(member, before, after)
    if op == "start":
        bot.dispatch("vc_start", member, after.channel)
    if op == "end":
        bot.dispatch("vc_end", before.channel)
    if op == "many":
        bot.dispatch("vc_many", member, after.channel)

@bot.event # 通話開始
async def on_vc_start(member: discord.Member, channel: discord.channel):
    emb = discord.Embed(title=f"{channel.name} で通話が開始されました！", description=f"{member.display_name}")
    chid = vc_funcs.detect_ch_id(channel.id)
    logger.info(f"VC_Start: {channel.name} is started.")
    await bot.get_channel(int(chid)).send(embed=emb)

@bot.event # 大人数参加
async def on_vc_many(member: discord.Member, channel: discord.channel):
    emb = discord.Embed(title=f"{channel.name} に {vc_funcs.count_people(channel)}人目の参加者がきました！", description=f"来た人: {member.display_name}")
    chid = vc_funcs.detect_ch_id(channel.id)
    logger.info(f"VC_Many: {member.display_name} is join to {channel.name}.")
    await bot.get_channel(int(chid)).send(embed=emb)

@bot.event
async def on_vc_end(channel: discord.channel):
    emb = discord.Embed(title=f"{channel.name} の通話は終了しました")
    chid = vc_funcs.detect_ch_id(channel.id)
    logger.info(f"VC_End: {channel.name} is ended.")
    await bot.get_channel(int(chid)).send(embed=emb)

@bot.slash_command(guild_ids=[GUILD_ID], description="指定のユーザーに援護ピンを立てます。")
async def engo(ctx, user : discord.User):
    msg = f"{user.mention}を援護！"
    logger.info(f"Slash_Engo: {msg}")
    await ctx.respond(msg)

bot.run(DISCORD_BOT_TOKEN)