import sys
sys.path.append('../')

import discord

# Load env
import libs.env as env

# Load DB
import libs.db as db
notice_channels = db.get_all_notice_channel_ids()

# Prepare logger
import libs.log as logger
def log(msg):
    logger.logger.info(msg)

# Prepare Bot
dc_intents = discord.Intents.all()
dc_intents.members = True

bot = discord.Bot(intents = dc_intents)

temp_category_name = "temporary"
temp_cat = None

# Set events
import disc.engo_pin.engo_pin
import disc.move_all.move_all
import disc.notice_channel.notice_channel
import disc.on_ready.on_ready
import disc.ping_pong.ping_pong
import disc.random_teaming.random_teaming
import disc.vc_notice.voice_state

# Run
bot.run(env.DISCORD_BOT_TOKEN)

