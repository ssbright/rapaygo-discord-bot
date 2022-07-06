import logging
import threading
import time

# import logging
# import threading
# import time
from variables import *
from api_handler import payment_confirmed_checker
from discord.ext import tasks




@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord #2!')
    channel = client.get_channel(int(CHANNEL_ID))
    await channel.send("Im Online a second time!")
    slow_count.start()


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
        print(curr_status)
        print(payHash)
        if (payment_confirmed_checker(payHash) == "COMPLETED") and (curr_status != "COMPLETED"):
            cur.execute(f"""update invoice_audit set status='COMPLETED' where payment_hash='{payHash}'""")
            conn.commit()
            channel = client.get_channel(int(CHANNEL_ID))
            await channel.send(f"{recipient} got tipped in Sats! ")
            print("payment shoudl have sent ")


# initiate the thread with daemon set to True#
#daemon_thread = threading.Thread(target=slow_count.start(), name="daemon-thread", daemon=True)

client.run(TOKEN)