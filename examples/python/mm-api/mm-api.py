#!/usr/bin/env python
# encoding: utf-8

import requests
import time
import urllib
import hashlib
import hmac
from web3 import Account
from zklink_sdk import ZkLinkLibrary, ZkLinkSigner
from zklink_sdk.types import Order, Token

domain_url = "http://domain_url"
eth_priv_key = ""
api_key = "your api key"
api_secret = "your api secret"


def server_info():
    path = "/mm/api/server"
    url = "%s%s" % (domain_url, path)
    resp = requests.get(url)
    print(resp.json())


def products_info():
    path = "/mm/api/products"
    url = "%s%s" % (domain_url, path)
    resp = requests.get(url)
    print(resp.json())


def get_jwt_token():
    args = {
        "timestamp": int(time.time())
    }
    headers = {
        "X-MBX-APIKEY": api_key
    }

    args_str = urllib.parse.urlencode(args)
    signature = hmac.new(bytes.fromhex(api_secret),
                         msg=args_str.encode("ascii"),
                         digestmod=hashlib.sha256) \
        .hexdigest().lower()
    path = "/mm/api/users?%s&signature=%s" % (args_str, signature)
    url = "%s%s" % (domain_url, path)
    resp = requests.get(url, headers=headers)
    print(resp.text)


def get_self_info():
    args = {
        "timestamp": int(time.time())
    }
    headers = {
        "X-MBX-APIKEY": api_key
    }

    args_str = urllib.parse.urlencode(args)
    signature = hmac.new(bytes.fromhex(api_secret),
                         msg=args_str.encode("ascii"),
                         digestmod=hashlib.sha256) \
        .hexdigest().lower()
    path = "/mm/api/self?%s&signature=%s" % (args_str, signature)
    url = "%s%s" % (domain_url, path)
    resp = requests.get(url, headers=headers)
    print(resp.text)


def get_slot_batchly(cnt):
    args = {
        "timestamp": int(time.time()),
        "count": cnt,
    }
    headers = {
        "X-MBX-APIKEY": api_key
    }

    args_str = urllib.parse.urlencode(args)
    signature = hmac.new(bytes.fromhex(api_secret),
                         msg=args_str.encode("ascii"),
                         digestmod=hashlib.sha256) \
        .hexdigest().lower()
    path = "/mm/api/slot?%s&signature=%s" % (args_str, signature)
    url = "%s%s" % (domain_url, path)
    resp = requests.get(url, headers=headers)
    print(resp.text)
    return resp.json()


def place_order(product_id, side, time_in_force, price, size,
                taker_fee_ratio, maker_fee_ratio, slot, nonce):
    assert side in ("BUY", "SELL")
    assert time_in_force in ("GTC", "IOC", "FOK", "GTX")

    account = Account.from_key(eth_priv_key)
    zksigner = ZkLinkSigner.from_account(account, ZkLinkLibrary())
    pubkey_hex = zksigner.public_key.hex()

    order = Order(
        account_id=7,     # from /mm/api/self
        price=int(price * (10 ** 18)),
        amount=int(size * (10 ** 18)),
        sub_account_id=1,
        slot=slot,
        nonce=nonce,
        base_token=Token(id=141, chain_id=0, address='', symbol='', decimals=18),   # from /mm/api/products
        quote_token=Token(id=1, chain_id=0, address='', symbol='', decimals=18),    # from /mm/api/products
        is_sell=0 if side == "BUY" else 1,
        taker_fee_ratio=taker_fee_ratio,
        maker_fee_ratio=maker_fee_ratio
    )

    order_signature_hex = zksigner.sign_order(order).signature
    args = {
        "timestamp": int(time.time()),
        "symbol": product_id,
        "side": side,
        "type": "LIMIT",
        "timeInForce": time_in_force,
        "price": int(price * (10 ** 18)),
        "quantity": int(size * (10 ** 18)),
        "takerFeeRatio": taker_fee_ratio,
        "makerFeeRatio": maker_fee_ratio,
        "slot": slot,
        "nonce": nonce,
        "userPubkey": pubkey_hex[2:] if pubkey_hex[0:2] == "0x" else pubkey_hex,
        "orderSignature": order_signature_hex[2:] if order_signature_hex[0:2] == "0x" else order_signature_hex
    }
    headers = {
        "X-MBX-APIKEY": api_key
    }

    args_str = urllib.parse.urlencode(args)
    signature = hmac.new(bytes.fromhex(api_secret),
                         msg=args_str.encode("ascii"),
                         digestmod=hashlib.sha256) \
        .hexdigest().lower()
    path = "/mm/api/orders?%s&signature=%s" % (args_str, signature)
    url = "%s%s" % (domain_url, path)
    resp = requests.post(url, headers=headers)
    print(resp.text)
    return resp.json().get("Id")


def cancel_order(product_id, order_id):
    args = {
        "timestamp": int(time.time()),
        "symbol": product_id,
        "orderId": order_id,
    }
    headers = {
        "X-MBX-APIKEY": api_key
    }

    args_str = urllib.parse.urlencode(args)
    signature = hmac.new(bytes.fromhex(api_secret),
                         msg=args_str.encode("ascii"),
                         digestmod=hashlib.sha256) \
        .hexdigest().lower()
    path = "/mm/api/order?%s&signature=%s" % (args_str, signature)
    url = "%s%s" % (domain_url, path)
    resp = requests.delete(url, headers=headers)
    print(resp.text)


def cancel_orders(product_id):
    args = {
        "timestamp": int(time.time()),
        "symbol": product_id,
    }
    headers = {
        "X-MBX-APIKEY": api_key
    }

    args_str = urllib.parse.urlencode(args)
    signature = hmac.new(bytes.fromhex(api_secret),
                         msg=args_str.encode("ascii"),
                         digestmod=hashlib.sha256) \
        .hexdigest().lower()
    path = "/mm/api/orders?%s&signature=%s" % (args_str, signature)
    url = "%s%s" % (domain_url, path)
    resp = requests.delete(url, headers=headers)
    print(resp.text)


def list_orders(product_id, start_time, end_time, limit):
    args = {
        "timestamp": int(time.time()),
        "symbol": product_id,
        "startTime": start_time,
        "endTime": end_time,
        "limit": limit,
    }
    headers = {
        "X-MBX-APIKEY": api_key
    }

    args_str = urllib.parse.urlencode(args)
    signature = hmac.new(bytes.fromhex(api_secret),
                         msg=args_str.encode("ascii"),
                         digestmod=hashlib.sha256) \
        .hexdigest().lower()
    path = "/mm/api/orders?%s&signature=%s" % (args_str, signature)
    url = "%s%s" % (domain_url, path)
    resp = requests.get(url, headers=headers)
    print(resp.text)


def get_order(product_id, order_id):
    args = {
        "timestamp": int(time.time()),
        "symbol": product_id,
        "orderId": order_id,
    }
    headers = {
        "X-MBX-APIKEY": api_key
    }

    args_str = urllib.parse.urlencode(args)
    signature = hmac.new(bytes.fromhex(api_secret),
                         msg=args_str.encode("ascii"),
                         digestmod=hashlib.sha256) \
        .hexdigest().lower()
    path = "/mm/api/order?%s&signature=%s" % (args_str, signature)
    url = "%s%s" % (domain_url, path)
    resp = requests.get(url, headers=headers)
    print(resp.text)


def list_open_orders(product_id, limit):
    args = {
        "timestamp": int(time.time()),
        "symbol": product_id,
        "limit": limit,
    }
    headers = {
        "X-MBX-APIKEY": api_key
    }

    args_str = urllib.parse.urlencode(args)
    signature = hmac.new(bytes.fromhex(api_secret),
                         msg=args_str.encode("ascii"),
                         digestmod=hashlib.sha256) \
        .hexdigest().lower()
    path = "/mm/api/openOrders?%s&signature=%s" % (args_str, signature)
    url = "%s%s" % (domain_url, path)
    resp = requests.get(url, headers=headers)
    print(resp.text)


def accounts_info():
    args = {
        "timestamp": int(time.time())
    }
    headers = {
        "X-MBX-APIKEY": api_key
    }

    args_str = urllib.parse.urlencode(args)
    signature = hmac.new(bytes.fromhex(api_secret),
                         msg=args_str.encode("ascii"),
                         digestmod=hashlib.sha256) \
        .hexdigest().lower()
    path = "/mm/api/accounts?%s&signature=%s" % (args_str, signature)
    url = "%s%s" % (domain_url, path)
    resp = requests.get(url, headers=headers)
    print(resp.text)


if __name__ == "__main__":
    server_info()
    products_info()
    get_jwt_token()
    get_self_info()
    slots = get_slot_batchly(5)
    order_id = place_order("wETH-USD", "BUY", "GTC", 300.0, 1.0, 10, 5, slots[0]["slot"], slots[0]["nonce"])
    cancel_order("wETH-USD", order_id)
    list_orders("wETH-USD", 0, int(time.time()), 10)
    get_order("wETH-USD", order_id)
    list_open_orders("wETH-USD", 10)
    accounts_info()
