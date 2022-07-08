# bot.py
import discord
import qrcode
import qrcode.image.svg




#local imports
from command_parser import command_validator
from api_handler import bot_commands
#from pay_status_thread import daemon_thread
from db.db import persist_invoice, persist_pos, check_user_exist, update_pos
from variables import *



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

    #This Chunck encapsulates DM messages
    if str.split(str(message.channel))[0] == 'Direct':
        if content.strip() == "hello":  # if the message is 'hello', the bot responds with 'Hi!'
            await user.send("Hi!")
        if command_validator(content) == True:
            #await user.send("I got your command!")
            cList = str.split(content)
            atBot = cList[0]
            command = cList[1]
            amount = cList[2]
            name = cList[3]
            # If..else for generating the invoice using the format @bot paid? {payment_hash} @recipient
            if command == "tip":
                bot_commands(command, amount, name)
                sender = message.author
                channelIn = 'DM'
                tokenDict = bot_commands(command, amount, name)
                #Now, bot checks if the recipient exists in rapaygo system
                if check_user_exist(str(name)) == True:
                    # adds row to databse for invoice generated
                    persist_invoice(tokenDict["invoice_id"], tokenDict["payment_hash"], name, sender, "tip", amount,channelIn)
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
                await user.send("So you want to register?!")
                key = cList[2]
                secret = cList[3]
                persist_pos(key, secret, user, user.id)
                await user.send("Ok! I successfully did so!")
            if command == "update":
                await user.send("So you want to update your keys?!")
                key = cList[2]
                secret = cList[3]
                update_pos(key, secret, user, user.id)
                await user.send("Ok! I successfully did so!")

                # Polling to see if invoice has been paid
    #This chunk encapsualtes non-DM messages
    else:
        if content.strip() == "hello":  # if the message is 'hello', the bot responds with 'Hi!'
            await channel.send("Hi!")
        if command_validator(content) == True:
            cList = str.split(content)
            atBot = cList[0]
            command = cList[1]
            amount = cList[2]
            name = cList[3]
            # If..else for generating the invoice using the format @bot paid? {payment_hash} @recipient
            if command == "tip":
                bot_commands(command, amount, name)
                sender = message.author
                channelIn = str(str.split(str(message.channel.id))[0])
                tokenDict = bot_commands(command, amount, name)

                if check_user_exist(str(name)) == True:
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
                    await channel.send(f"Hey {name}! {sender} wants to tip you in Sats! However, you are not currently registered with rapaygo. If you feel like getting tipped, please go to this website:  https://rapaygo.com/. Once you make an account, generate a POS key. There will be two keys (line1 and line2). Then DM in the format: @rapaygo-paybot register line1_key line2_key. Once you do that, you can get tipped in Sats!_")

        pass


  






client.run(TOKEN)

