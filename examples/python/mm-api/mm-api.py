#!/usr/bin/env python
# encoding: utf-8

import requests
import time
import urllib
import hashlib
import hmac

domain_url = "http://domain_url"
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
    signature = hmac.new(api_secret.encode("ascii"),
                         msg=args_str.encode("ascii"),
                         digestmod=hashlib.sha256) \
        .hexdigest().lower()
    path = "/mm/api/users?%s&signature=%s" % (args_str, signature)
    url = "%s%s" % (domain_url, path)
    resp = requests.get(url, headers=headers)
    print(resp.text)


def get_slot():
    args = {
        "timestamp": int(time.time())
    }
    headers = {
        "X-MBX-APIKEY": api_key
    }

    args_str = urllib.parse.urlencode(args)
    signature = hmac.new(api_secret.encode("ascii"),
                         msg=args_str.encode("ascii"),
                         digestmod=hashlib.sha256) \
        .hexdigest().lower()
    path = "/mm/api/slot?%s&signature=%s" % (args_str, signature)
    url = "%s%s" % (domain_url, path)
    resp = requests.get(url, headers=headers)
    print(resp.text)


def place_order(product_id, side, time_in_force, price, size,
                taker_fee_ratio, maker_fee_ratio, slot, nonce, order_signature_hex):
    assert side in ("BUY", "SELL")
    assert time_in_force in ("GTC", "IOC")
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
        "orderSignature": order_signature_hex[2:] if order_signature_hex[0:2] == "0x" else order_signature_hex
    }
    headers = {
        "X-MBX-APIKEY": api_key
    }

    args_str = urllib.parse.urlencode(args)
    signature = hmac.new(api_secret.encode("ascii"),
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
    signature = hmac.new(api_secret.encode("ascii"),
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
    signature = hmac.new(api_secret.encode("ascii"),
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
    signature = hmac.new(api_secret.encode("ascii"),
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
    signature = hmac.new(api_secret.encode("ascii"),
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
    signature = hmac.new(api_secret.encode("ascii"),
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
    signature = hmac.new(api_secret.encode("ascii"),
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
    get_slot()
    order_id = place_order("JOE-USD", "BUY", "GTC", 300.0, 1.0, 10, 5, 3, 100,
                           "08df5d62219ec5c77d75d178e553371d10b166f0288e61e0186818de459502093d135821e6100f4fb8a4fda5ff17bef776a9dc855dd5b68809ab77e052c20902")
    cancel_order("JOE-USD", order_id)
    # cancel_orders("JOE-USD")
    list_orders("JOE-USD", 0, int(time.time()), 10)
    get_order("JOE-USD", order_id)
    list_open_orders("JOE-USD", 10)
    accounts_info()
