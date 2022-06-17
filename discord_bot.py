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
from threading import Thread 
import polling2

#local imports
from command_parser import command_validator
from api_handler import bot_commands, payment_confirmed_checker


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
            tokenDict= bot_commands(command, amount, name)
            await channel.send("Here is your payment request: ```{}```".format(tokenDict["payment_request"]))
            #await channel.send("Here is a link to the decoder: https://lightningdecoder.com/{}".format(tokenDict["payment_request"]))
            qr = qrcode.make(tokenDict["payment_request"])
            qrimage = qr.save("invoice.png")
            #await channel.send("And here is your QR code!")
            await channel.send(file=discord.File("invoice.png"))
            os.remove("./invoice.png")

            #Polling to see if invoice has been paid 
            def is_paid_responce(response):
                    return response == "COMPLETED"

            def poll_pay():
                polling2.poll (  
                lambda : payment_confirmed_checker(tokenDict["payment_hash"]),
                check_success = is_paid_responce,
                max_tries=100,
                step = 1 ,
                ignore_exceptions=(IOError,),
                )

    
            thread = Thread(target=poll_pay)


            thread.start()
            #await channel.send("Waiting for payment...")

            thread.join()
            await channel.send("You have been paid!")
        
        else:
            pass
        #If..else for generating the invoice using the format @bot paid? {payment_hash} @recipient 
        if command == "paid?":
            responceDict= bot_commands(command, amount, name)
            if responceDict["status"] == "COMPLETED":
                await channel.send("Yup! You have been paid!")
            else:
                await channel.send("Sorry, you have not been paid yet. Status is:{}".format(responceDict["status"]))
    else:
        print("Sorry, I do not understand this command.")




client.run(TOKEN)