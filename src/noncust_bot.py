# bot.py
import psycopg2
from dotenv import load_dotenv
import os
from discord.ext import commands
from discord_slash import SlashCommand
import lnd_grpc
import qrcode
import qrcode.image.svg
import discord


#local imports
from command_parser import command_validator, inquiry_command, anyother_message

#from pay_status_thread import daemon_thread
from db.db import check_user_status

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_PERSONAL')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
CHANNEL_ID= os.getenv('DISCORD_CHANNEL_ID_TEST')
BOT_ID=os.getenv('DISCORD_BOT_ID')
LND_FOLDER=os.getenv('LND_FOLDER')
LND_MACAROON_FILE= os.getenv('LND_MACAROON_FILE')
LND_TLS_CERT_FILE=os.getenv('LND_TLS_CERT_FILE')
LND_RPC_HOST=os.getenv('LND_RPC_HOST')

client = commands.Bot(command_prefix="!")
slash = SlashCommand(client, sync_commands=True)

conn = psycopg2.connect("dbname='rapaygo_invoice' user='sydney'")
cur = conn.cursor()

lnd_rpc = lnd_grpc.Client(
    lnd_dir=LND_FOLDER,
    macaroon_path=LND_MACAROON_FILE,
    tls_cert_path=LND_TLS_CERT_FILE,
    grpc_host=LND_RPC_HOST,

)

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


helpMessage='''
             Yo! 
             My main purpose is to generate invoices so you can tip someone in Bitcoin Satoshis! The only way to talk to me is to @mention me at the begging of your message (no need to @mention me if in DM). To tip someone type a message in this format:
             @rapaygo-paybot tip [enter number of sats] @[the discord user]
             for example:
             @rapaygo-paybot tip 200 @rapaygo-paybot
             This would send 200 satoshis to myself!
             
             I also have some DM only commands:
             I can only generate an invoice to send funds if the recipient is signup up for rapaygo. To do this please go to https://rapaygo.com/. Once an account is made, generate a pos key. Then DM like this:
             register <API Key> <API Key Secret> 
             If you want to update your keys, becuase they only last for a specified amount of time you can repeat the process in the DM like so:
             update <API Key> <API Key Secret> 
             You can ask me if you are registered by typing:
             status
             
             
             '''


@client.event
async def on_message(message):  # this event is called when a message is sent by anyone
    # this is the string text message of the Message
    content = message.content
    # this is the sender of the Message
    user = message.author
    # this is the channel of there the message is sent
    channel = client.get_channel(int(message.channel.id))

    # if the user is the client user itself, ignore the message
    if user == client.user:
        return

    print("Received a message:", content)
    #This Chunck encapsulates DM messages
    if str.split(str(message.channel))[0] == 'Direct':
        content2 ="<@1016751469900337162> " + str(content)
        if content.strip() == "hello":  # if the message is 'hello', the bot responds with 'Hi!'
            await user.send("Hi!")
        if content.strip() == "Hello":  # if the message is 'hello', the bot responds with 'Hi!'
            await user.send("Hi!")
        if inquiry_command(content2) == 1:
            await user.send(helpMessage)
        if inquiry_command(content2) == 2:
            cList = str.split(content2)
            await user.send("So you are wondering if you are registered with rapaygo? Give me one moment please.")
            user = message.author
            if check_user_status(user) == True:
                await user.send("Yup! You are registered!")
            else:
                await user.send("Sorry, you are not registered yet! Please type help to learn how to register")

        if anyother_message(content2) == True:
            await user.send("Sorry, I didnt understand that. Type in: help. That way I can explain to you how I work")
        if command_validator(content2) == True:
            #await user.send("I got your command!")
            cList = str.split(content2)
            command = cList[1]
            amount = cList[2]
            recipient = cList[3]
            # If..else for generating the invoice using the format @bot paid? {payment_hash} @recipient
            #if command == "tip":
                #REPLACE THIS!!!



                # Polling to see if invoice has been paid

    #This chunk encapsualtes non-DM messages
    else:
        if content.strip() == "hello":  # if the message is 'hello', the bot responds with 'Hi!'
            await channel.send("Hi!")
      #  if content.strip() == "test":  # if the message is 'hello', the bot responds with 'Hi!'
      #      get_access_token(user)
      #      await channel.send("Hi!")
        if inquiry_command(content) == 1:
            await channel.send(helpMessage)

        if anyother_message(content) == True:
            print("another message is TRUE")
            await channel.send("Sorry, I didnt understand that. Type in: @rapaygo-paybot help. That way I can explain to you how I work")
        if command_validator(content) == True:
            print("command validator is TRUE")
            cList = str.split(content)
            command = cList[1]
            amount = cList[2]
            name = cList[3]
            # If..else for generating the invoice using the format @bot paid? {payment_hash} @recipient
            if command == "tip":
                print("invoice triggered")
                await channel.send("invoice triggered")
                user = message.author
                lnd_rpc.add_invoice("Invoice from discord user {}".format(user), int(amount), 3600);
                invoices = lnd_rpc.list_invoices()
                qr = qrcode.make(invoices.invoices._values[-1].payment_request)
                qr.save("invoice.png")
                await channel.send("Here is your payment request: ```{}```".format(invoices.invoices._values[-1].payment_request),
                                file=discord.File("invoice.png"))

                # print(lnd_rpc.list_invoices());
                await channel.send("invoice made!")
                os.remove("./invoice.png")
        pass









client.run(TOKEN)

