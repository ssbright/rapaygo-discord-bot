import logging
import threading
import time

# import logging
# import threading
# import time
from variables import *
from api_handler import payment_confirmed_checker
from discord.ext import tasks


global user
global channel
global content




@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord #2!')
    channel = client.get_channel(int(CHANNEL_ID))
    await channel.send("Im Online a second time!")
    slow_count.start()

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

@tasks.loop(seconds=5.0)
async def slow_count():


    # cur.execute("""select id from invoice_audit where status= 'PENDING'""")
    cur.execute("""select * from invoice_audit""")
    query_results = cur.fetchall()




    for row in query_results:

        # print(f"inspect row {row}")
        payHash = row[4]
        curr_status = row[9]
        recipient = row[6]
        channelID = row[10]
        print(curr_status)
        print(payHash)
        if (payment_confirmed_checker(payHash) == "COMPLETED") and (curr_status != "COMPLETED"):

            if channelID == 'DM':
                cur.execute(f"""update invoice_audit set status='COMPLETED' where payment_hash='{payHash}'""")
                conn.commit()
                altRecipient = recipient[2:-1]
                user = await client.fetch_user(int(altRecipient))
                print(altRecipient)
                print(type(altRecipient))
                print(user)
                print(type(user))
                await user.send(f"{recipient} got tipped in Sats! ")
                print("payment shoudl have sent ")
            else:
                cur.execute(f"""update invoice_audit set status='COMPLETED' where payment_hash='{payHash}'""")
                conn.commit()
                channel = client.get_channel(int(channelID))
                await channel.send(f"{recipient} got tipped in Sats! ")
                print("payment shoudl have sent ")






# initiate the thread with daemon set to True#
#daemon_thread = threading.Thread(target=slow_count.start(), name="daemon-thread", daemon=True)

client.run(TOKEN)