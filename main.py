from lib2to3.pgen2 import token
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.environ['APP_BOT_TOKEN']
DISCORD_CLIENT_ID = os.environ['CLIENT_ID']
NOTICE_CH_ID = int(os.environ['NOTICE_CH_ID'])
UNITE_TX_ID = int(os.environ['UNITE_TX_ID'])
UNITE_VC_ID = int(os.environ['UNITE_VC_ID'])
GENSHIN_TX_ID = int(os.environ['GENSHIN_TX_ID'])
GENSHIN_VC_ID = int(os.environ['GENSHIN_VC_ID'])
GUILD_ID = [int(os.environ['GUILD_ID'])]

import discord

intents=discord.Intents.all() # after

# client = discord.Client()
bot = discord.Bot(intents = intents)

@bot.event
async def on_message(message):
    msg = message.content
    print("on_message: " + message.content + " (" + message.channel.name + ")")
    res = ""

    if msg == "ping":
        res = "pong"
    if msg == "hong":
        res = "kong"
    if msg == "bang":
        res = "kok"
    if msg == "にゃが":
        res = "にゃがにゃが"
    
    if res != "":
        await message.channel.send(res)
    
@bot.event
async def on_ready():
    print("listening...")

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None: # Start検知
        id = after.channel.id
        ch = bot.get_channel(id)
        cnt = len(ch.voice_states.keys())

        if cnt == 1: # 通話が開始された
            bot.dispatch("vc_start",member,after.channel)

    if before.channel is not None: # End判定
        id = before.channel.id
        ch = bot.get_channel(id)
        cnt = len(ch.voice_states.keys())
        
        if cnt == 0: # 通話が終了した
            bot.dispatch("vc_end",member,before.channel)

@bot.event
async def on_vc_start(member, channel):
    msg = f"{member.display_name}が{channel.name}に来たようです！"
    print(msg)

    chid = NOTICE_CH_ID

    if str(channel.id) == str(UNITE_VC_ID): # UNITE部
        chid = UNITE_TX_ID
    if str(channel.id) == str(GENSHIN_VC_ID): # 原神部
        chid = GENSHIN_TX_ID
    
    await bot.get_channel(int(chid)).send(msg)

@bot.event
async def on_vc_end(member, channel):
    msg = f"{channel.name}の通話は終了しました。"
    print(msg)

    chid = NOTICE_CH_ID

    if str(channel.id) == str(UNITE_VC_ID): # UNITE部
        chid = UNITE_TX_ID
    if str(channel.id) == str(GENSHIN_VC_ID): # 原神部
        chid = GENSHIN_TX_ID
    
    await bot.get_channel(int(chid)).send(msg)

bot.run(DISCORD_BOT_TOKEN)