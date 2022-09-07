# bot.py
import discord
import qrcode
import qrcode.image.svg
import psycopg2
from dotenv import load_dotenv
import os
from discord.ext import commands
from discord_slash import SlashCommand




#local imports
from command_parser import command_validator, inquiry_command, anyother_message

from api_handler import bot_commands
#from pay_status_thread import daemon_thread
from db.db import persist_invoice, persist_pos, check_user_exist, check_user_status, update_pos

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_TEST')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
CHANNEL_ID= os.getenv('DISCORD_CHANNEL_ID_TEST')
BOT_ID=os.getenv('DISCORD_BOT_ID')

client = commands.Bot(command_prefix="!")
slash = SlashCommand(client, sync_commands=True)

conn = psycopg2.connect("dbname='rapaygo_invoice' user='sydney'")
cur = conn.cursor()


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
        content2 ="<@984815715544617011> " + str(content)
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
            if command == "tip":
                tokenDict = bot_commands(command, amount, recipient)
                sender = message.author
                channelIn = 'DM'
               # tokenDict = bot_commands(command, amount, name)
                #Now, bot checks if the recipient exists in rapaygo system
                if check_user_exist(str(recipient)) == True:
                    # adds row to databse for invoice generated
                    persist_invoice(tokenDict["invoice_id"], tokenDict["payment_hash"], sender, recipient, "tip", amount,channelIn)
                    qr = qrcode.make(tokenDict["payment_request"])
                    qrimage = qr.save("invoice.png")
                    # await channel.send("And here is your QR code!")
                    #await user.send(file=discord.File("invoice.png"))

                    await user.send("Here is your payment request: ```{}```".format(tokenDict["payment_request"]),file=discord.File("invoice.png"))
                    # await channel.send("Here is a link to the decoder: https://lightningdecoder.com/{}".format(tokenDict["payment_request"]))
                    os.remove("./invoice.png")
                else:
                    await user.send(
                '''
                Sorry, I do not know who that is. That being said, if you would like to share with them this link: https://rapaygo.com/, they could sign up to recieve tips. Full instructions are listed here for how to set me up. I would do this myself, however I am a bot who refuses to spam other people's DMs.
                '''
                )

            if command == "register":
                await user.send("So you want to register?! Give me one moment, if I don't reply soon, I might have bugs.")
                key = cList[2]
                secret = cList[3]
                persist_pos(key, secret, user, user.id)
                await user.send("Ok! I successfully did so!")
            if command == "update":
                await user.send("So you want to update your keys?! Give me one moment, if I don't reply soon, I might have bugs.")
                key = cList[2]
                secret = cList[3]
                update_pos(key, secret, user, user.id)
                await user.send("Ok! I successfully did so!")

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
            await channel.send(
                "Sorry, I didnt understand that. Type in: @rapaygo-paybot help. That way I can explain to you how I work")
        if command_validator(content) == True:
            cList = str.split(content)
            command = cList[1]
            amount = cList[2]
            name = cList[3]
            # If..else for generating the invoice using the format @bot paid? {payment_hash} @recipient
            if command == "tip":

                sender = message.author
                if check_user_exist(str(name)) == True:
                    tokenDict = bot_commands(command, amount, name)

                    channelIn = str(str.split(str(message.channel.id))[0])
                    # tokenDict = bot_commands(command, amount, name)
                    # adds row to databse for invoice generated
                    persist_invoice(tokenDict["invoice_id"], tokenDict["payment_hash"], name, sender, "tip", amount, channelIn)

                    qr = qrcode.make(tokenDict["payment_request"])
                    qrimage = qr.save("invoice.png")
                    # await channel.send("And here is your QR code!")
                    #await user.send(file=discord.File("invoice.png"))

                    await channel.send("Here is your payment request: ```{}```".format(tokenDict["payment_request"]),file=discord.File("invoice.png"))
                    # await channel.send("Here is a link to the decoder: https://lightningdecoder.com/{}".format(tokenDict["payment_request"]))
                    os.remove("./invoice.png")
                else:
                    await channel.send("Sorry I don't know who this is!")
                    await channel.send(f"Hey {name}! {sender} wants to tip you in Sats! However, you are not currently registered with rapaygo. If you feel like getting tipped, please go to this website:  https://rapaygo.com/. Once you make an account, generate a POS key. There will be two keys (API Key and API Key Secret). Then DM in the format: @rapaygo-paybot register line1_key line2_key. Once you do that, you can get tipped in Sats!_")

        pass


  






client.run(TOKEN)

