from trycourier import Courier

client = Courier(auth_token="pk_prod_XYZ")
#  make this a secret key
# REMEMBER - to use this I will have to update the token, save as an environment variable - this is just a dummy token.

resp = client.send_message(
  message={
    "to": {
      "email": "lauren.perini@gmail.com",
    },
    "template": "YV95GRTJQS4VQVH2QATKPBVV4PDC",
    "data": {
      "recipientName": "Lauren",
      "productName": "Define Jacket Luon",
      "productColor": "Magenta Purple",
      "productPrice":"118",
      "productSize": "2",
      "productURL": "https://shop.lululemon.com/p/jackets-and-hoodies-jackets/Define-Jacket?color=54428&sz=2"
    },
  }
)

print(resp['requestId'])