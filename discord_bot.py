# bot.py
import discord
import qrcode
import qrcode.image.svg




#local imports
from command_parser import command_validator
from api_handler import bot_commands
#from pay_status_thread import daemon_thread
from db.db import persist_invoice
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

    if content.strip() == "hello":  # if the message is 'hello', the bot responds with 'Hi!'
        await channel.send("Hi!")

  
    if  command_validator(content) == True:
        await channel.send("I got your command!")
        cList = str.split(content)
        atBot = cList[0]
        command = cList[1]
        amount  = cList[2]
        name = cList[3]
        #If..else for generating the invoice using the format @bot paid? {payment_hash} @recipient 
        if command == "tip":
            bot_commands(command, amount, name)
            sender = message.author
            tokenDict= bot_commands(command, amount, name)

            #adds row to databse for invoice generated
            persist_invoice(tokenDict["invoice_id"], tokenDict["payment_hash"], name, sender, "tip", amount)

            await channel.send("Here is your payment request: ```{}```".format(tokenDict["payment_request"]))
            #await channel.send("Here is a link to the decoder: https://lightningdecoder.com/{}".format(tokenDict["payment_request"]))
            qr = qrcode.make(tokenDict["payment_request"])
            qrimage = qr.save("invoice.png")
            #await channel.send("And here is your QR code!")
            await channel.send(file=discord.File("invoice.png"))
            os.remove("./invoice.png")

            #Polling to see if invoice has been paid 


#daemon_thread.start()


client.run(TOKEN)

