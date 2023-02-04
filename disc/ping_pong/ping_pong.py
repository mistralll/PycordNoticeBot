import sys
sys.path.append('../')

import disc.bot as bot

@bot.bot.event
async def on_message(message):
    if message.author.bot:
        return
    res = make_res(message.content)
    if res != "":
        bot.log(f"PingPong: {res}")
        await message.channel.send(res)

def make_res(msg):
    res = ""

    if msg == "ping":
        res = "pong"
    if msg == "hong":
        res = "kong"
    if msg == "bang":
        res = "kok"
    if msg == "溜めて":
        res = "解放"

    if msg.count("にゃが") > 0:
        cnt = msg.count("にゃが")
        res = "にゃが"
        for _ in range(cnt):
            res += "にゃが"

    return res