# bot.py
import os
import discord
import discord_slash
from dotenv import load_dotenv
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option 
import qrcode
import qrcode.image.svg

#local imports
from command_parser import command_validator
from api_handler import invoice_generator


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
CHANNEL_ID= os.getenv('DISCORD_CHANNEL_ID')
BOT_ID=os.getenv('DISCORD_BOT_ID')

client = commands.Bot(command_prefix="!")
slash = SlashCommand(client, sync_commands=True)



@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(int(CHANNEL_ID))
    await channel.send("Im Online!")


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )




@client.event
async def on_message(message):  # this event is called when a message is sent by anyone
    # this is the string text message of the Message
    content = message.content
    # this is the sender of the Message
    user = message.author
    # this is the channel of there the message is sent
    channel = client.get_channel(int(CHANNEL_ID))

    # if the user is the client user itself, ignore the message
    if user == client.user:
        return

    print("Received a message:", content)

    if  command_validator(content) == True:
        await channel.send("I got your command!")
        cList = str.split(content)
        atBot = cList[0]
        command = cList[1]
        amount  = cList[2]
        name = cList[3]

        payment_req = invoice_generator(command, amount, name)
        await channel.send("Here is your payment request: ```{}```. Here is a link to the decoder: https://lightningdecoder.com/{}".format(payment_req, payment_req))

        qr = qrcode.make(payment_req)
        qrimage = qr.save("invoice.png")
        await channel.send("And here is your QR code!")
        await channel.send(file=discord.File("invoice.png"))
        os.remove("./invoice.png")
        

    else:
        print("Sorry, I do not understand this command.")


    if content.strip() == "hello":  # if the message is 'hello', the bot responds with 'Hi!'
        await channel.send("Hi!")





#@raypaygobot tip 200 @brightman11

"""
@slash.slash(
    name="hello",
    description="Just sends a message",
    guild_ids=[974081336866373724]
)
async def _hello(ctx:SlashContext):
    await ctx.send("World!")
"""


client.run(TOKEN)