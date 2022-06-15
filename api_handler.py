from ast import Pass
import requests 
import json
import os
from dotenv import load_dotenv

url = "https://api.rapaygo.com/v1/auth/access_token"

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

response1 = requests.request("POST", url, data=json.dumps(payload))

#print(response.text)


tokenDict = json.loads(response1.text)

accessToken = tokenDict["access_token"]


#Invoice Generator 

def invoice_generator(command, amount, recipient):
  if command == "tip":
    url = "https://api.rapaygo.com/v1/invoice_payment/ln/invoice"

    payload = {
        "amount_sats" : "{}".format(amount),
        "memo" : "rapaygo POS invoice",
    }

    headers = {
      'Authorization': accessToken
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))

    print(response.text)
    tokenDict = json.loads(response.text)
    payment_req = tokenDict["payment_request"]
    return payment_req
  else:
    return False

