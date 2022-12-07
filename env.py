# Prepare env variable
import os
from dotenv import load_dotenv
load_dotenv()
DISCORD_BOT_TOKEN = os.environ['APP_BOT_TOKEN']
DISCORD_CLIENT_ID = os.environ['CLIENT_ID']
GUILD_ID = int(os.environ['GUILD_ID'])