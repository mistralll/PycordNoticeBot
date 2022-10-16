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

import discord

#intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)  #before
intents=discord.Intents.all() # after

client = discord.Client()
bot = discord.Bot()

@client.event
async def on_message(message):
    if message.content == "ping":
        await message.channel.send("pong")

@client.event
async def on_ready():
    print("listening...")

@client.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None: # Start検知
        id = after.channel.id
        ch = client.get_channel(id)
        cnt = len(ch.voice_states.keys())

        if cnt == 1: # 通話が開始された
            client.dispatch("vc_start",member,after.channel)

    if before.channel is not None: # End判定
        id = before.channel.id
        ch = client.get_channel(id)
        cnt = len(ch.voice_states.keys())
        
        if cnt == 0: # 通話が終了した
            client.dispatch("vc_end",member,before.channel)

@client.event
async def on_vc_start(member, channel):
    msg = f"{member.display_name}が{channel.name}に来たようです！"
    print(msg)

    chid = NOTICE_CH_ID

    if str(channel.id) == str(UNITE_VC_ID): # UNITE部
        chid = UNITE_TX_ID
    if str(channel.id) == str(GENSHIN_VC_ID): # 原神部
        chid = GENSHIN_TX_ID
    
    await client.get_channel(int(chid)).send(msg)

@client.event
async def on_vc_end(member, channel):
    msg = f"{channel.name}の通話は終了しました。"
    print(msg)

    chid = NOTICE_CH_ID

    if str(channel.id) == str(UNITE_VC_ID): # UNITE部
        chid = UNITE_TX_ID
    if str(channel.id) == str(GENSHIN_VC_ID): # 原神部
        chid = GENSHIN_TX_ID
    
    await client.get_channel(int(chid)).send(msg)

client.run(DISCORD_BOT_TOKEN)