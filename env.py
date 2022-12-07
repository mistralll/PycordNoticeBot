# Prepare env variable
import os
from dotenv import load_dotenv
load_dotenv()
DISCORD_BOT_TOKEN = os.environ['APP_BOT_TOKEN']
DISCORD_CLIENT_ID = os.environ['CLIENT_ID']
GUILD_ID = int(os.environ['GUILD_ID'])
HOST = os.environ['DB_HOST']
USER = os.environ['DB_USER']
PASS = os.environ['DB_PASS']
NAME = os.environ['DB_NAME']
PORT = os.environ['DB_PORT']