from ast import Pass
import requests 
import json
import os
from dotenv import load_dotenv



url1 = "https://api.rapaygo.com/v1/auth/access_token"

load_dotenv()
Password = os.getenv('PASS')

payload = {
    "username" : "Ssbright11@gmail.com",
    "pass_phrase" : Password,
    "type" : "pos_user"
}
headers = {
  'Authorization': ''
}

response1 = requests.request("POST", url1, data=json.dumps(payload))

#print(response.text)


tokenDict = json.loads(response1.text)

accessToken = tokenDict["access_token"]




def bot_commands(command, amount, recipient):
  #Invoice Generator Command
  if command == "tip":
    url2 = "https://api.rapaygo.com/v1/invoice_payment/ln/invoice"

    payload = {
        "amount_sats" : "{}".format(amount),
        "memo" : "rapaygo POS invoice",
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
    #Payment verifidier

    url3 = "https://api.rapaygo.com/v1/invoice_payment/by_payment_hash/{}".format(amount)

    payload = {
      "amount_sats" : "200",
      "memo" : "rapaygo POS invoice",
    }

    headers = {
      'Authorization': '',
      'Accept': 'application/json'
    }

    response = requests.request("GET", url3, headers=headers, data=payload)
    responceDict = json.loads(response.text)
    payment_stat = responceDict["status"]
    print(response.text)
    return responceDict

  else:
    return False,


def payment_confirmed_checker(pay_hash):
  #Payment verifidier

    url3 = "https://api.rapaygo.com/v1/invoice_payment/by_payment_hash/{}".format(pay_hash)

    payload = {
      "amount_sats" : "200",
      "memo" : "rapaygo POS invoice",
    }

    headers = {
      'Authorization': '',
      'Accept': 'application/json'
    }

    response = requests.request("GET", url3, headers=headers, data=payload)
    responceDict = json.loads(response.text)
    payment_stat = responceDict["status"]


    
    return payment_stat