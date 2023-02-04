import sys
sys.path.append('../')
import disc.bot as bot

@bot.bot.event
async def on_ready():
    bot.log("Ready!")

