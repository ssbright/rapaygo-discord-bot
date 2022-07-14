from ast import Pass
import requests
import json
import os
from dotenv import load_dotenv
import psycopg2


def get_access_token(user):
  conn = psycopg2.connect("dbname='rapaygo_invoice' user='sydney'")
  cur = conn.cursor()
  cur.execute('select * from user_pos')
  conn.commit()

  user_table = cur.fetchall()


  url1 = "https://api.rapaygo.com/v1//auth/key"

  load_dotenv()

  for row in user_table:
    discord_name = row[5]
    if str(user) == str(discord_name):
      email = row[3]
      password = row[4]
      payload = {
        "key": email,
        "secret": password
      }

      headers = {
        'Authorization': ''
      }
      response1 = requests.request("POST", url1, data=json.dumps(payload))
      tokenDict = json.loads(response1.text)
      accessToken = tokenDict["access_token"]
      return accessToken
    else:
      pass

  conn.close()



def bot_commands(user ,command, amount, recipient):
  # Invoice Generator Command
  accessToken = get_access_token(user)
  if command == "tip":
    url2 = "https://api.rapaygo.com/v1/invoice_payment/ln/invoice"

    payload = {
      "amount_sats": "{}".format(amount),
      "memo": "rapaygo POS invoice",
    }

    headers = {
      'Authorization': accessToken
    }
    response = requests.request("POST", url2, headers=headers, data=json.dumps(payload))

    print(response.text)
    tokenDict = json.loads(response.text)
    payment_req = tokenDict["payment_request"]
    payment_hash = tokenDict["payment_hash"]
    return tokenDict


  elif command == "paid?":
    # Payment verifidier

    url3 = "https://api.rapaygo.com/v1/invoice_payment/by_payment_hash/{}".format(amount)

    payload = {
      "amount_sats": "200",
      "memo": "rapaygo POS invoice",
    }

    headers = {
      'Authorization': '',
      'Accept': 'application/json'
    }

    response = requests.request("GET", url3, headers=headers, data=payload)
    responceDict = json.loads(response.text)
    '''
    {"checking_id":"c12fe9b17e8b8ab7b04acc4829190c14cb0f7a18fe3d740afcf0b818706d1e27",
    "invoice_id":2649,
    "message":"Invoice created",
    "payment_hash":"c12fe9b17e8b8ab7b04acc4829190c14cb0f7a18fe3d740afcf0b818706d1e27",
    "payment_request":"lnbc1u1p32ekwlpp5cyh7nvt73w9t0vz2e3yzjxgvzn9s77sclc7hgzhu7zupsurdrcnshp56mgev926f9h2f88f9l78at6js6klpz8juh52zm9ehrr3pyr9selqcqzpgxqyz5vqsp5z00pnwvnthjf8vzqj6agxjjp4zqhdcvmd4c4lk37fc4s4kvsv2cq9qyyssqp25m27udn776te00s4032kyq50p27ctcf7feyty0s6w452zjvvtntgw2xhh9zv0nglxd5rjhm3y6l8ygc0ghsqy8n3xupxvugfyaxvgqk8zqrc"}
    '''
    payment_stat = responceDict["status"]
    print(response.text)
    return responceDict

  else:
    return False,


def payment_confirmed_checker(pay_hash):
  # Payment verifidier

  url3 = "https://api.rapaygo.com/v1/invoice_payment/by_payment_hash/{}".format(pay_hash)

  payload = {
    "amount_sats": "200",
    "memo": "rapaygo POS invoice",
  }

  headers = {
    'Authorization': '',
    'Accept': 'application/json'
  }

  response = requests.request("GET", url3, headers=headers, data=payload)
  responceDict = json.loads(response.text)
  '''
  {"amount":200,
  "checking_id":"3ca2f50e55c98b25734fd8306bf8dbd0c11da70369948d45a6cccb84cf72a92e",
  "created_at":"2022-06-15 23:23:21.154171",
  "created_at_ts":1655335401.154171,
  "extra":"",
  "fee":0,
  "id":2610,
  "ln_fee":0,
  "lnurl_payment_id":null,
  "memo":"7c686 POS payment. rapaygo POS invoice",
  "msat_amount":200000,
  "msat_fee":0,
  "msat_ln_fee":0,
  "msat_tx_fee":2000,
  "payment_hash":"3ca2f50e55c98b25734fd8306bf8dbd0c11da70369948d45a6cccb84cf72a92e",
  "payment_request":"lnbc2u1p32560fpp58j302rj4ex9j2u60mqcxh7xm6rq3mfcrdx2g63dxen9cfnmj4yhqhp56mgev926f9h2f88f9l78at6js6klpz8juh52zm9ehrr3pyr9selqcqzpgxqyz5vqsp5everph8kx3wsgzw5d4u3zruhkwlyj0adm7sux829zyf0cu6n270s9qyyssqrmtpmr86j3vr9luczu3g2d7zzt625y26wlp3uz23pqvw26gvcnkkw7pklempcyt7k4lvgp90fay0vfq0v3daqdt7ccq5dne038zf0tsqgqqmwr",
  "pending":false,
  "pending_int":0,
  "preimage":"",
  "status":"COMPLETED",
  "tx_fee":2,
  "updated_at":"2022-06-15 23:23:58.636452",
  "wallet_id":141,
  "webhook":"",
  "webhook_external_id":null,
  "webhook_status":"pending",
  "withdraw_voucher_id":null}
  '''

  payment_stat = responceDict["status"]

  return payment_stat