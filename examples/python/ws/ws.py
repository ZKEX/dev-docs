#!/usr/bin/env python
# encoding: utf-8


from websocket import create_connection
import json
import requests
import time
import urllib
import hashlib
import hmac

domain_url = "http://domain_url"
ws_url = "ws://ws_url"
api_key = "your api key"
api_secret = "your api secret"

PRODUCTS = ['JOE-USD', 'QUICK-USD']
ASSETS = ['JOE', 'QUICK', 'USD']

products_str = ','.join([json.dumps(p) for p in PRODUCTS])
assets_str = ','.join([json.dumps(p) for p in ASSETS])

snap_level2_subscribe_tpl = '''
{
  "type": "subscribe",
  "product_ids": [
    %s
  ],
  "channels": [
    "level2"
  ],
  "token": ""
}
'''

candles_1m_subscribe_tpl = '''
{
  "type": "subscribe",
  "product_ids": [
    %s
  ],
  "channels": [
    "candles_1m"
  ],
  "token": ""
}
'''

ticker_subscribe_tpl = '''
{
  "type": "subscribe",
  "product_ids": [
    %s
  ],
  "channels": [
    "ticker"
  ],
  "token": ""
}
'''

match_subscribe_tpl = '''
{
  "type": "subscribe",
  "product_ids": [
    %s
  ],
  "channels": [
    "match"
  ],
  "token": ""
}
'''

trade_subscribe_tpl = '''
{
  "type": "subscribe",
  "product_ids": [
    %s
  ],
  "channels": [
    "trade"
  ],
  "token": "%s"
}
'''

order_subscribe_tpl = '''
{
  "type": "subscribe",
  "product_ids": [
    %s
  ],
  "channels": [
    "order"
  ],
  "token": "%s"
}
'''

funds_subscribe_tpl = '''
{
  "type": "subscribe",
  "currency_ids": [
    %s
  ],
  "channels": [
    "funds"
  ],
  "token": "%s"
}
'''


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
    return resp.text


def websocket_maintaining_loop():
    jwt_token = get_jwt_token()

    ws_ep = create_connection(ws_url)
    ws_ep.send(snap_level2_subscribe_tpl % products_str)
    ws_ep.send(candles_1m_subscribe_tpl % products_str)
    ws_ep.send(ticker_subscribe_tpl % products_str)
    ws_ep.send(match_subscribe_tpl % products_str)
    ws_ep.send(trade_subscribe_tpl % (products_str, jwt_token))
    ws_ep.send(order_subscribe_tpl % (products_str, jwt_token))
    ws_ep.send(funds_subscribe_tpl % (assets_str, jwt_token))

    while True:
        msg = ws_ep.recv()
        print(msg)


if __name__ == "__main__":
    websocket_maintaining_loop()

