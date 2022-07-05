import psycopg2
from dotenv import load_dotenv
import os
from discord.ext import commands
from discord_slash import SlashCommand


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
CHANNEL_ID= os.getenv('DISCORD_CHANNEL_ID')
BOT_ID=os.getenv('DISCORD_BOT_ID')

client = commands.Bot(command_prefix="!")
slash = SlashCommand(client, sync_commands=True)

conn = psycopg2.connect("dbname='rapaygo_invoice' user='sydney'")
cur = conn.cursor()