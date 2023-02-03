import discord

def count_people(vc: discord.VoiceChannel):
    # Return how many people is in voice channel.
    # If voice channel is None, return -1.
    if vc == None: return -1
    return len(vc.voice_states.keys())

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
