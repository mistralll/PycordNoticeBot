import sys
sys.path.append('../')

import discord
import disc.libs.voice_channel as lib

def detect_operation(bf:discord.VoiceState, af:discord.VoiceState):
    # When voice state is updated, then return next operation.
    # Return "start", "end" or "many" normally.
    # Return -1 when error happen.
    bf_cnt = lib.count_people(bf.channel)
    af_cnt = lib.count_people(af.channel)

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