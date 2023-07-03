#!/usr/bin/env python
# encoding: utf-8
from web3 import Account
from zklink_sdk import ZkLinkLibrary, ZkLinkSigner
from zklink_sdk.types import Order, Token
import urllib
import requests

ETH = 141
USD = 1
size = "10000000000000000"
l2UserId = 8

auth_jwt_token = ""
eth_priv_key = ""

headers = {
    "Access-Token": auth_jwt_token
}

###########################################################################################

priceURL = "https://dev-v1-acc.zkex.com/api-v1/api/flashExchange/askPrice"
priceArgs = {
    "baseTokenId": ETH,
    "quoteTokenId": USD,
    "baseExchange": size
}
priceReq = urllib.parse.urlencode(priceArgs)
resp = requests.get("%s?%s" % (priceURL, priceReq), headers=headers)
print(resp.text)
price = resp.json()["price"]
print(price)

###########################################################################################

slotURL = "https://dev-v1-acc.zkex.com/api-v1/api/slot"
resp = requests.get(slotURL, headers=headers)
slot, nonce = resp.json()["slot"], resp.json()["nonce"]
print(slot, nonce)

###########################################################################################

account = Account.from_key(eth_priv_key)
zksigner = ZkLinkSigner.from_account(account, ZkLinkLibrary())
pubkey_hex = zksigner.public_key.hex()

order = Order(
    account_id=l2UserId,
    price=int(price),
    amount=int(size),
    sub_account_id=1,
    slot=slot,
    nonce=nonce,
    base_token=Token(id=ETH, chain_id=0, address='', symbol='', decimals=18),
    quote_token=Token(id=USD, chain_id=0, address='', symbol='', decimals=18),
    is_sell=1,
    taker_fee_ratio=10,
    maker_fee_ratio=5
)

order_signature_hex = zksigner.sign_order(order).signature

placeOrderArgs = {
    "price": price,
    "size": size,
    "funds": str(int(price) * int(size) / (10 ** 18)),
    "side": "sell",
    "l2UserId": l2UserId,
    "slot": slot,
    "nonce": nonce,
    "l2baseCurrencyId": ETH,
    "l2quoteCurrencyId": USD,
    "makerFeeRatio": 5,
    "takerFeeRatio": 10,
    "pubkey": pubkey_hex[2:] if pubkey_hex[0:2] == "0x" else pubkey_hex,
    "signature": order_signature_hex[2:] if order_signature_hex[0:2] == "0x" else order_signature_hex
}

print(pubkey_hex)
print(order_signature_hex)

placeURL = "https://dev-v1-acc.zkex.com/api-v1/api/flashExchange/placeFlashOrder"
resp = requests.post(placeURL, json=placeOrderArgs, headers=headers)
print(resp.json())
