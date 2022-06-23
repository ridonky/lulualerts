from trycourier import Courier
import json

from retail_alerts.settings import AUTH_TOKEN

client = Courier(auth_token=AUTH_TOKEN)
#  make this a secret key
# # REMEMBER - to use this I will have to update the token, save as an environment variable - this is just a dummy token.

# resp = client.send_message(
#   message={
#     "to": {
#       "email": "lauren.perini@gmail.com",
#     },
#     "template": "YV95GRTJQS4VQVH2QATKPBVV4PDC",
#     "data": {
#       "recipientName": "Lauren",
#       "productName": "Define Jacket Luon",
#       "productColor": "Magenta Purple",
#       "productPrice":"118",
#       "productSize": "2",
#       "productURL": "https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=54428&sz=2"
#     },
#   }
# )

# print(resp['requestId'])
# print(resp)


import requests


# test id with error
# id = "1-62b32add-26d06416e13ff0246787dcde"

# test id that succeeds
id = "1-62b32a1a-99ee9b7c86445d8f802b8bc8"
url = (f"https://api.courier.com/messages/{id}")

headers = {
  "Accept": "application/json",
  "Authorization":f"Bearer {AUTH_TOKEN}"
}

response = requests.request("GET", url, headers=headers)


print(json.loads(response.text)["status"])
