import discord

import os
from dotenv import load_dotenv
load_dotenv()
NOTICE_CH_ID = int(os.environ['NOTICE_CH_ID'])
UNITE_TX_ID = int(os.environ['UNITE_TX_ID'])
UNITE_VC_ID = int(os.environ['UNITE_VC_ID'])
GENSHIN_TX_ID = int(os.environ['GENSHIN_TX_ID'])
GENSHIN_VC_ID = int(os.environ['GENSHIN_VC_ID'])

def count_people(vc: discord.VoiceChannel):
    # Return how many people is in voice channel.
    # If voice channel is None, return -1.
    if vc == None: return -1
    return len(vc.voice_states.keys())

def detect_operation(bf:discord.VoiceState, af:discord.VoiceState):
    # When voice state is updated, then return next operation.
    # Return is "start", "end" or "many" normally.
    # Return -1 when error happen.
    bf_cnt = count_people(bf.channel)
    af_cnt = count_people(af.channel)

    is_dif_ch = True
    if bf_cnt != -1 and af_cnt != -1:
        is_dif_ch = bf.channel.id is af.channel.id

    if af_cnt != -1:
        if bf_cnt == -1 and af_cnt == 1:
            return "start"
        if af_cnt > 3 and is_dif_ch and bf_cnt < af_cnt:
            return "many"
    if bf_cnt == 0:
        return "end"
    return -1

def detect_ch_id(chid: int):
    # Return text channel id.
    # When arg is Unite or Genshin voice channel id, return corresponding text channel id.
    if chid == UNITE_VC_ID:
        return UNITE_TX_ID
    if chid == GENSHIN_VC_ID:
        return GENSHIN_TX_ID
    return NOTICE_CH_ID