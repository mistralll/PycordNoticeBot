import discord
import random_teaming

def count_people(vc: discord.VoiceChannel):
    # Return how many people is in voice channel.
    # If voice channel is None, return -1.
    if vc == None: return -1
    return len(vc.voice_states.keys())

def detect_operation(bf:discord.VoiceState, af:discord.VoiceState):
    # When voice state is updated, then return next operation.
    # Return "start", "end" or "many" normally.
    # Return -1 when error happen.
    bf_cnt = count_people(bf.channel)
    af_cnt = count_people(af.channel)

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

def detect_ch_id(list, chid: int):
    tmp = -1
    default = -1
    for row in list:
        if row[0] == "default":
            default = row[1]
        if row[0] == str(chid):
            tmp = row[1]

    if tmp != -1:
        return tmp
    else:
        return default
