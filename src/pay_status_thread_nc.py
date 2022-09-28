# import logging
# import threading
import time
from api_handler import payment_confirmed_checker
from discord.ext import tasks
import asyncio
from lndgrpc import AsyncLNDClient
from google.protobuf.json_format import MessageToDict
import configparser
from dotenv import load_dotenv
import os
from discord.ext import commands
from discord_slash import SlashCommand
import psycopg2

global user
global channel
global content

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_PERSONAL')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = os.getenv('DISCORD_GUILD_ID')
CHANNEL_ID= os.getenv('DISCORD_CHANNEL_ID_TEST')
BOT_ID=os.getenv('DISCORD_BOT_ID')

client = commands.Bot(command_prefix="!")
slash = SlashCommand(client, sync_commands=True)
config = configparser.ConfigParser()
config.read(os.path.join(os.getcwd(), 'ini/config.ini'))
conn = psycopg2.connect("dbname='rapaygo_invoice' user='sydney'")
cur = conn.cursor()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord #2!')
    channel = client.get_channel(int(CHANNEL_ID))
    await channel.send("Im Online a second time!")
    await run()

@tasks.loop(seconds=5.0)
async def subscribe_invoices():
    cur.execute(f"""select distinct(channel) from invoice_audit_nc""")
    all_channels = cur.fetchall()
    for channelID in all_channels:
        # Deine the RPC client for specifc channel from config file
        LND_RPC_PORT = config[str(channelID[0])]['LND_NODE_PORT']
        LND_RPC_IP = config[str(channelID[0])]['LND_NODE_IP']
        LND_FOLDER = config[str(channelID[0])]['LND_FOLDER']
        LND_MACAROON_FILE = config[str(channelID[0])]['LND_MACAROON_FILE']
        LND_TLS_CERT_FILE = config[str(channelID[0])]['LND_TLS_CERT_FILE']
        LND_RPC_HOST = config[str(channelID[0])]['LND_RPC_HOST']
        lnd_ip_port = f"{LND_RPC_IP}:{LND_RPC_PORT}"

        async_lnd = AsyncLNDClient(
            ip_address=lnd_ip_port,
            cert_filepath=LND_TLS_CERT_FILE,
            macaroon_filepath=LND_MACAROON_FILE
        )
        print('Listening for invoices...')
        async for invoice in async_lnd.subscribe_invoices():
            #print(invoice)
            dict_obj = MessageToDict(invoice,
                                     including_default_value_fields=True,
                                     preserving_proto_field_name=True)
            print(dict_obj["payment_request"])
            print(dict_obj["state"])
            #if dict_obj["state"]:
            #    print(" state is false")
            time.sleep(0.5) #Wait very breifly for bot to persist to POSTGRES server
            cur.execute(f"""select * from invoice_audit_nc where payment_hash = '{dict_obj["payment_request"]}'""")
            query_results = cur.fetchall()
            print(query_results)

            for row in query_results:
                # print(f"inspect row {row}")
                payHash = row[3]
                curr_status = row[8]
                recipient = row[5]
                channelID = row[9]
                if (dict_obj["state"] == "SETTLED") and (curr_status != "COMPLETED"):
                    print("working so far settled")

                    cur.execute(f"""update invoice_audit_nc set status='COMPLETED' where payment_hash='{dict_obj["payment_request"]}'""")
                    conn.commit()
                    channel = client.get_channel(int(channelID))
                    print(channelID)
                    print(channel)
                    print(recipient)
                    await channel.send(f"{recipient} got tipped in Sats! ")
                    print("payment sent ")


async def run():
    coros = [subscribe_invoices()]
    await asyncio.gather(*coros)

client.run(TOKEN)
#loop = asyncio.get_event_loop()
#loop.run_until_complete(run())


