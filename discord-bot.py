# Application ID - 984815715544617011
# Public Key - f3544dc0ff418c17305993ee9bf2b86b6bb5dcccbdf29d067e10485a83d363f8
# Permission Integer - 8
#generated URL https://discord.com/api/oauth2/authorize?client_id=984815715544617011&permissions=8&scope=bot

# bot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

class CustomClient(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

client = CustomClient()
""" 
@client.event
async def on_ready():
    guild = discord.utils.find(lambda g: g.name == GUILD, client.guilds)
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
"""
client.run(TOKEN)