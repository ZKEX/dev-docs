
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Maintain trading pairs information](#maintain-trading-pairs-information)
- [REST Interface (Recommend)](#)
  - [Get the server time of ZKEX](#get-the-server-time-of-zkex)
  - [Get all trading pairs supported by ZKEX](#get-all-trading-pairs-supported-by-zkex)
  - [Get Market Maker's JWT-Token (use to subscribe Websocket)](#mmregister)
  * [New Order](#mmplaceorder)
  * [Cancel Order](#mmcancelorder)
  * [Cancel all Open Orders on a Symbol](#mmcancelorders)
  * [Get all orders](#mmgetorders)
  * [Get all open orders ](#mmgetopenorders)
  * [Query Order](#mmgetorder)
  * [Account Info](#mmgetaccounts)

- [REST Interface (Like binance api)](#)
- [Websocket Subscribe & Unsubscribe ](#websocket-subscribe--unsubscribe)
  - [Subscribe or unsubscribe order data of any trading pair](#ws-level2)
  - [Subscribe or unsubscribe K-line data of a trading pair](#ws-candles)
  - [Subscribe or unsubscribe ticker info of a trading pair ](#ws-ticker)
  - [Subscribe or unsubscribe matching information of a trading pair](#ws-match)
  - [Subscribe or unsubscribe success order information of a trading pair](#ws-trade)
  - [Subscribe or unsubscribe order change infomation of a trading pair](#ws-order)
  - [Subscribe or unsubscribe the asset change information of an account](#ws-funds)
- [Websocket Data Push](#websocket-data-push)
  * [Overview](#overview)
  * [Push the snapshot of any pair](#push-snapshot)
  * [Push current price change of any pair](#push-l2update)
  * [Push K-line data of any pair](#push-candles)
  * [Push ticker infomation of any pair](#push-ticker)
  * [Push matching infomation of an account](#push-match)
  * [Push trading infomation](#push-trade)
  * [Push order change infomation of a trading pair](#push-order)
  * [Push the asset change infomation of an account](#push-funds)


## Getting Started
<span id='prerequisites'></span>
- Prerequisites

  * address
  * active address
  * apply to ZKEX Team to get `api key` and `api secret`
  * depoly `market maker signer service` and send `signer url` to ZKEX Team

--- 

<span id='maintain-trading-pairs-information'></span>
- Maintain trading pairs information

  * Get all trading pairs infomation through the `REST` interface [BnGetProducts](#bngetproducts)
  * Get any trading pair infomation through `ws`, subscribe channel [ws-level2](#ws-level2)
  * When you subscribe to [ws-level2](#ws-level2) for the first time, you will receive the snapshot data by [push-snapshot](#push-snapshot)
  * When the data of the [ws-level2](#ws-level2) changes, you will receive the data in the type of [l2update](#l2update)

## REST Interface (Recommend)
<span id='get-the-server-time-of-zkex'></span>
- Get the server time of ZKEX

  - Http Method : `GET`
  - Http Path : `/mm/api/server`
  - Response : 
    ```json
    {
      "timeNow": 1650958799 
    }
    ```
    
---

<span id="get-all-trading-pairs-supported-by-zkex"></span>
- Get all trading pairs supported by ZKEX

  - Http Method : `GET`
  - Http Path : `/mm/api/products`
  - Response : 
  
    <details>
    <summary>data</summary>
    
    ```json
    [
        {
            "id": "XNY-USDT",
            "baseCurrency": "XNY",
            "quoteCurrency": "USDT",
            "baseMinSize": "10000000000000",      //base asset minimal amount
            "baseMaxSize": "10000000000000000000000000",    //unused
            "quoteIncrement": "10000000000000000",      //quote asset minimal amount
            "baseScale": -12,              //decimals
            "quoteScale": -16,      //decimals
            "l2symbolId": 2,                  // trading pair id on layer2
            "l2baseCurrencyId": 3,          // currency id on layer2
            "l2quoteCurrencyId": 4        // currency id on layer2
        },
        ......
    ]   
    ```
    </details>
 
---

<span id="mmregister"></span>
* Get Market Maker's JWT-Token (use to subscribe Websocket)
  * HTTP Method: `GET`
  * HTTP Path: `/mm/api/users`  (HMAC SHA256)
  * HTTP Header:
    `X-MBX-APIKEY` :  `api key`
  * Parameters:
  
    | **_Name_**  	| **_Type_** 	| **_Required_** 	| **_Example_**        	| **_Description_**      	|
    |-------------	|:----------:	|:--------------:	|----------------------	|------------------------	|
    | timestamp   	|    long    	|       YES      	| 1653983486           	| unix timestamp         	|
   
  * Response :
    ```
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhZGRyZXNzIjoiMHgzNDk4ZjQ1NjY0NTI3MGVlMDAzNDQxZGY4MmM3MThiNTZjMGU2NjY2IiwiZXhwaXJlZEF0IjoxNjU0MDU1MDMzLCJpZCI6NDksInB1YmtleSI6IjBkZDRmNjAzNTMxYmQ3OGJiZWNkMDA1ZDllN2NjNjJhNzk0ZGNmYWRjZWZmZTAzZTI2OWZiYjZiNzJlOWM3MjQifQ.2S1wt6KxfJU8kxvESbrdUW1jxYyqxXlcIhL9DwtW3Yc
    ```

---


<span id="mmplaceorder"></span>
* New Order
  * Send in a new order.
  * HTTP Method: `POST`
  * HTTP Path: `/mm/api/orders`  (HMAC SHA256)
  * HTTP Header:
    `X-MBX-APIKEY` : `api key`
  * API Limit: A single account is only allowed to send maximum of 30 new order per second
    
  * Parameters: 
  
    | **_Name_**  	| **_Type_** 	| **_Required_** 	| **_Example_**        	| **_Description_**      	|
    |-------------	|:----------:	|:--------------:	|----------------------	|------------------------	|
    | symbol      	|   string   	|       YES      	| UNI-USDC             	| The trading pair name  	|
    | side        	|   string   	|       YES      	| SELL                 	| SELL/BUY               	|
    | type        	|   string   	|       YES      	| LIMIT                	| only support LIMIT now 	|
    | timestamp   	|    long    	|       YES      	| 1654060757           	| unix timestamp         	|
    | timeInForce 	|   string   	|       YES      	| GTC                  	| GTC/IOC                	|
    | quantity    	|   string   	|       YES      	| 20000000000000000000 	| decimals=18            	|
    | price       	|   string   	|       YES      	| 5000000000000000000  	| decimals=18            	|

  
  * Response
  
    ```json
    {
      "Id": 39,
      "CreatedAt": 1650958799,
      "UpdatedAt": 1650958799,
      "ProductId": "UNI-USDT",
      "UserId": 1,
      "ClientOid": "",
      "Size": "1000000000000000000",        
      "Funds": "70000000",
      "FilledSize": "0",
      "ExecutedValue": "0", 
      "Price": "70000000", 
      "FillFees": "0",
      "Type": "limit",
      "Side": "buy",
      "TimeInForce": "GTC",     
      "Status": "new",
      "Settled": false
    }   
    ```

-------------------------------

<span id="mmcancelorder"></span>
* Cancel Order
  * Cancel an active order
  * HTTP Method: `DELETE`
  * HTTP Path: `/mm/api/order`   (HMAC SHA256)
  * HTTP Header:
    `X-MBX-APIKEY` : `api key`

  * Parameters
  
    | **_Name_**  	| **_Type_** 	| **_Required_** 	| **_Example_**        	| **_Description_**      	|
    |-------------	|:----------:	|:--------------:	|----------------------	|------------------------	|
    | timestamp   	|    long    	|       YES      	| 1654060757           	| unix timestamp         	|
    | symbol      	|   string   	|       YES      	| UNI-USDC             	| The trading pair name  	|
    | orderId       |   int     	|       YES      	| 755                	  |  	|
    

  * Response: none

-------------------------------

<span id="mmcancelorders"></span>
* Cancel all Open Orders on a Symbol
  * HTTP Meth: `DELETE`
  * HTTP PATH: `/mm/api/orders`   (HMAC SHA256)
  * HTTP HEADER:
    `X-MBX-APIKEY` : `api key`

  * Parameters:
    
    | **_Name_**  	| **_Type_** 	| **_Required_** 	| **_Example_**        	| **_Description_**      	|
    |-------------	|:----------:	|:--------------:	|----------------------	|------------------------	|
    | timestamp   	|    long    	|       YES      	| 1654060757           	| unix timestamp         	|
    | symbol      	|   string   	|       YES      	| UNI-USDC             	| The trading pair name  	|
    

  * Response : none

-------------------------------

<span id="mmgetorders"></span>
* Get all orders
  * Get all orders, includes `new`, `open`,  `filled`, `cancelled`, `cancelling`
  * HTTP Method: `GET`
  * HTTP PATH: `/mm/api/orders`   (HMAC SHA256)
  
  * HTTP HEADER:
    `X-MBX-APIKEY` : `api key`

  * Parameters:
  
    | **_Name_**  	| **_Type_** 	| **_Required_** 	| **_Example_**        	| **_Description_**      	|
    |-------------	|:----------:	|:--------------:	|----------------------	|------------------------	|
    | timestamp   	|    long    	|       YES      	| 1654060757           	| unix timestamp         	|
    | symbol      	|   string   	|       YES      	| UNI-USDC             	| The trading pair name  	|
    | startTime        	|   long   	|       YES      	| 1                 	|                	|
    | endTime        	|   long   	|       YES      	| 1654063467                	| 	|
    | limit 	|   int   	|       YES      	| 20                  	|                	|

  * Response: 
  
    <details>
      <summary>data</summary>
  
      ```json
      {
        "total": 1000,
        "orders": [{
          "id": "28",          # order id
          "price": "9000000000000000",         
          "size": "2500000000",           
          "funds": "19997",                # price*size/pow(10,18)
          "productId": "UNI-USDT",
          "side": "sell",               # buy or sell
          "type": "limit",                
          "createdAt": 1650958799,
          "fillFees": "0",              
          "filledSize": "200000000",                 # The actual transaction quantity of the order
          "executedValue": "1800000",              # The actual transaction value of the order
          "status": "open",                   #order status   `new`, `open`,  `filled`, `cancelled`, `cancelling`
          "settled": false,
          "chanFrom": 0,             #     0 : user order       1 : market maker order
          "trades": [{
           "id": 1,
           "time": 1650958799,
           "tradeSeq": 231628,
           "price": "9000000000000000",
           "takerOrderId": 3,
           "makerOrderId": 4,
           "size": "100000",
           "side": "buy",
           "status": 3    # 0:not sent to layer2      1:sent to layer2      2:layer2 success    3:layer2 fail      9:matching fail(not sent to layer2)
          }, {
           "id": 2,
           "time": 1650958799,
           "tradeSeq": 231627,
           "price": "9000000000000000",
           "takerOrderId": 3,
           "makerOrderId": 4, 
           "size": "100000",
           "side": "buy",
           "status": 3
          }],
          "cancelFill": {
           "id": 1,
           "time": 1650958799,
           "size": "199800000",
           "doneReason": "cancelled"
          }
          "isFullFill": true,   # If isFullFill is true, it means that the order has actually been filled completely. But `trade.status` may not be `filled` , but it will eventually become filled.
         }, {
          "id": "27",
          "price": "8000000000000000",
          "size": "2500000000",
          "funds": "0",
          "productId": "BTC-USDT",
          "side": "buy",
          "type": "limit",
          "createdAt": 1650958799,
          "fillFees": "0",
          "filledSize": "0",
          "executedValue": "0",
          "status": "cancelled",
          "settled": false,
          "trades": [{
           "id": 1,
           "time": 1650958799,
           "tradeSeq": 231628,
           "price": "8000000000000000",
           "takerOrderId": 3,
           "makerOrderId": 4,
           "size": "100000",
           "side": "buy",
           "status": 3 
          }, {
           "id": 2,
           "time": 1650958799,
           "tradeSeq": 231627,
           "price": "8000000000000000",
           "takerOrderId": 3,
           "makerOrderId": 4,
           "size": "100000",
           "side": "buy",
           "status": 3
          }]
          "cancelFill": {
           "id": 1,
           "time": 1650958799,
           "size": "199800000",
           "doneReason": "cancelled"
         },
         "isFullFill": true   
        }]
       }    
      ```


-------------------------------


<span id="mmgetorder"></span>
* Query Order
  * Check an order's status.
  * HTTP Method: `GET`
  * HTTP PATH: `/mm/api/order`  (HMAC SHA256)
  * HTTP Header:
    `X-MBX-APIKEY` : `api key`

  * Parameters
  
    | **_Name_**  	| **_Type_** 	| **_Required_** 	| **_Example_**        	| **_Description_**      	|
    |-------------	|:----------:	|:--------------:	|----------------------	|------------------------	|
    | timestamp   	|    long    	|       YES      	| 1654060757           	| unix timestamp         	|
    | symbol      	|   string   	|       YES      	| UNI-USDC             	| The trading pair name  	|
    | orderId       |   int     	|       YES      	| 755                	  |  	|
    
  * Response
  
    <details>
      <summary>data</summary>
  
      ```json
      {
          "id": "755",     
          "price": "9000000000000000",            
          "size": "2500000000",                
          "funds": "19997",              
          "productId": "UNI-USDT",
          "side": "sell",             
          "type": "limit",                      
          "createdAt": 1650958799,
          "fillFees": "0",                 
          "filledSize": "200000000",                
          "executedValue": "1800000",             
          "status": "open",              
          "settled": false,
          "chanFrom": 0,              
          "trades": [{
           "id": 1,
           "time": 1650958799,
           "tradeSeq": 231628,
           "price": "9000000000000000",
           "takerOrderId": 3,
           "makerOrderId": 4,
           "size": "100000",
           "side": "buy",
           "status": 3  
          }, {
           "id": 2,
           "time": 1650958799,
           "tradeSeq": 231627,
           "price": "9000000000000000",
           "takerOrderId": 3,
           "makerOrderId": 4, 
           "size": "100000",
           "side": "buy",
           "status": 3
          }],
          "cancelFill": {
           "id": 1,
           "time": 1650958799,
           "size": "199800000",
           "doneReason": "cancelled"
          },
          "isFullFill": true 
      }
      ```

-------------------------------

<span id="mmgetopenorders"></span>
* Get all open orders 
  * HTTP Method: `GET`
  * HTTP Path: `/mm/api/openOrders`  (HMAC SHA256)
  * HTTP Header:
    `X-MBX-APIKEY` : `api key`
    
  * Parameters: 
  
    | **_Name_**  	| **_Type_** 	| **_Required_** 	| **_Example_**        	| **_Description_**      	|
    |-------------	|:----------:	|:--------------:	|----------------------	|------------------------	|
    | timestamp   	|    long    	|       YES      	| 1654060757           	| unix timestamp         	|
    | symbol      	|   string   	|       YES      	| UNI-USDC             	| The trading pair name  	|
    | limit 	|   int   	|       YES      	| 20                  	|                	|

  * Response : [same as  Get all orders Response](#mmgetorders)
  

-------------------------------

<span id="mmgetaccounts"></span>
* Account Info
  * HTTP Method: `GET`
  * HTTP Path: `/mm/api/accounts`
  * HTTP HEADER:
    `X-MBX-APIKEY` : `api key`
    
  * Parameters: 
  
    | **_Name_**  	| **_Type_** 	| **_Required_** 	| **_Example_**        	| **_Description_**      	|
    |-------------	|:----------:	|:--------------:	|----------------------	|------------------------	|
    | timestamp   	|    long    	|       YES      	| 1654060757           	| unix timestamp         	|


  * Response
      
    ```json
    [
      {
       "id": "1",
       "currency": "USDC",
       "currencyIcon": "https://raw.githubusercontent.com/Uniswap/assets/master/blockchains/ethereum/assets/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48/logo.png",
       "available": "952011220000",
       "hold": "1030410000000"
      }, {
       "id": "2",
       "currency": "USDT",
       "currencyIcon": "https://raw.githubusercontent.com/trustwallet/assets/master/blockchains/ethereum/assets/0xdAC17F958D2ee523a2206206994597C13D831ec7/logo.png",
       "available": "4444030410000000",
       "hold": "766652011220000"
      }
    ]    
    ```

------

## REST Interface (Like binance api)

### TODO

## Websocket Subscribe & Unsubscribe 

<span id="ws-level2"></span>
- Subscribe or unsubscribe order data of any trading pair (`level2`)
  - Subscribe

    ```json
    {
      "type": "subscribe",                                
      "product_ids": [
        "UNI-USDC"
      ],
      "channels": [
        "level2"
      ],
      "token": "" #option
    }
    ```
  - Unsubscribe
    ```json
    {
      "type": "unsubscribe",                                
      "product_ids": [
        "UNI-USDC"
      ],
      "channels": [
        "level2"
      ],
      "token": "" #option
    }
    ```
  - Notice
  
    When you subscribe to [level2](#ws-level2) for the first time, you will receive the snapshot data by [push-snapshot](#push-snapshot)
    
-----
      

<span id="ws-candles"></span>
* Subscribe or unsubscribe K-line data of a trading pair (1/3/5/15/30/60min/2/4/6/12/24hour)

  * Subscribe
    ```json
    {
      "type": "subscribe",                                
      "product_ids": [
        "UNI-USDC"
      ],
      "channels": [
        "candles_1m"
      ],
      "token": ""   # optional (JWT-token)
    }
    ```

  * Unsubscribe
    ```json
    {
      "type": "unsubscribe",                                
      "product_ids": [
        "UNI-USDC"
      ],
      "channels": [
        "candles_1m"
      ],
      "token": ""    # optional (JWT-token)
    }
    ```
  
  * Channel name comparison table
  
    | channel name | time |
    | ----   | ---- |
    |candles_1m    | 1min    |
    |candles_3m    | 3min |
    |candles_5m    | 5min   | 
    |candles_15m   | 15min   | 
    |candles_30m   | 30min   | 
    |candles_60m   | 60min   | 
    |candles_120m  | 2hour    | 
    |candles_240m  | 4hour    | 
    |candles_360m  | 6hour    | 
    |candles_720m  | 12hour   | 
    |candles_1440m | 24hour   |

-------------------------------

<span id="ws-ticker"></span>
* Subscribe or unsubscribe ticker info of a trading pair 
  * Subscribe
    ```json
    {
      "type": "subscribe",                                
      "product_ids": [
        "UNI-USDC"
      ],
      "channels": [
        "ticker"
      ],
      "token": ""    # optional (JWT-token)
    }
    ```

  * Unsubscribe
    ```json
    {
      "type": "unsubscribe",                                
      "product_ids": [
        "UNI-USDC"
      ],
      "channels": [
        "ticker"
      ],
      "token": ""    # optional (JWT-token)
    }
    ```
  
-------------------------------

<span id="ws-match"></span>
* Subscribe or unsubscribe matching information of a trading pair
     
  * Subscribe
    ```json
    {
      "type": "subscribe",                                
      "product_ids": [
        "UNI-USDC"
      ],
      "channels": [
        "match"
      ],
      "token": ""    # optional (JWT-token)
    }
    ```

  * Unsubscribe
    ```json
    {
      "type": "unsubscribe",                                
      "product_ids": [
        "UNI-USDC"
      ],
      "channels": [
        "match"
      ],
      "token": ""    # optional (JWT-token)
    }
    ```


-------------------------------

<span id="ws-trade"></span>
* Subscribe or unsubscribe success order information of a trading pair
  * Subscribe
    ```json
    {
      "type": "subscribe",                                
      "product_ids": [
        "UNI-USDC"
      ],
      "channels": [
        "trade"
      ],
      "token": ""    # required (JWT-token) 
    }
    ```

  * Unsubscribe
    ```json
    {
      "type": "unsubscribe",                                
      "product_ids": [
        "UNI-USDC"
      ],
      "channels": [
        "trade"
      ],
      "token": ""    # required (JWT-token)
    }
    ```


-------------------------------

<span id="ws-order"></span>
* Subscribe or unsubscribe order change infomation of a trading pair
  * Subscribe
    ```json
    {
      "type": "subscribe",                                
      "product_ids": [
        "UNI-USDC"
      ],
      "channels": [
        "order"
      ],
      "token":""  # required (JWT-token)
    }
    ```

  * Unsubscribe
    ```json
    {
      "type": "unsubscribe",                                
      "product_ids": [
        "UNI-USDC"
      ],
      "channels": [
        "order"
      ],
      "token": ""  # required (JWT-token)
    }
    ```


-------------------------------

<span id="ws-funds"></span>
* Subscribe or unsubscribe the asset change information of an account
  * Subscribe
    ```json
    {
      "type": "subscribe",                                
      "currency_ids": [
        "UNI",
        "USDC"
      ],
      "channels": [
        "funds"
      ],
      "token": ""   # required (JWT-token)
    }
    ```

  * Unsubscribe
    ```json
    {
      "type": "unsubscribe",                                
      "currency_ids": [
        "UNI",
        "USDC"
      ],
      "channels": [
        "funds"
      ],
      "token":""   # required (JWT-token)
    }
    ```



## Websocket Data Push
      
      
<span id="overview"></span>
- Overview        
  * How to get [push-snapshot](#push-snapshot)
    * When you subscribe to [level2](#ws-level2) for the first time, you will receive the snapshot data by [push-snapshot](#push-snapshot)
    * If you want to get snapshot multiple times, you can unsubscribe first, and then continue to subscribe
  * Unfilled order and cancel order
    * Maker will receive [push l2update](#push-l2update), [push order](#push-order), [push funds](#push-funds)
    * Others will receive [push l2update](#push-l2update)
  * Filled order
    * Maker and taker will receive [push l2update](#push-l2update), [push order](#push-order), [push funds](#push-funds), [push match](#push-match), [push ticker](#push-ticker), [push trade](#push-trade)
    * Others will receive [push l2update](#push-l2update), [push ticker](#push-ticker), [push match](#push-match)
  * [push trade](#push-trade) response contains the following 4 kinds of status
    * status = 0, matching success
    * status = 2, layer2 tx success
    * status = 3, layer2 tx fail
    * status = 9, failed to build layer2 transaction

---

<span id="push-snapshot"></span>
- Push snapshot data 
  - Subscribe channel : `level2`
  - Push only once, when the `level2` channel is established

  <details>
    <summary>data</summary>
    
    ```json
        {
     "type": "snapshot",
     "productId": "UNI-USDC",
     "bids": [
       [
         "200000000",   // price            
         "10000000000000",      // order size(amount)
         1         // (order count)
       ],
       [
         "10000000000",
         "10000000000000",
         1
       ]
     ],
     "asks": [
       [
         "90000000000",
         "10000000000000",
         1
       ],
       [
         "9000000000000",
         "10000000000000",
         1
       ],
       [
         "100000000000000",
         "10000000000000",
         1
       ],
       [
         "1100000000000000",
         "10000000000000",
         1
       ]
     ]
    }

    ```
    </details>
    
----
<span id="push-l2update"></span>
- Push data changes
  - Subscribe channel : `level2`
  ```json
    {
     "type": "l2update",
     "productId": "UNI-USDC",
     "changes": [
       [
         "sell",
         "90000000000000000000",  // price
         "100000000000"     // amount
       ]
     ]
    }
  ```
  
---

<span id="push-candles"></span>
* Push K-line data
   * Subscribe channel: `candles_1m`,`candles_3m`,`candles_5m`....
   * Maximum 1 push within 1s
  ```json
  {
   "type": "candles_1m",
   "productId": "UNI-USDC",
   "time": 1653273480,
   "open":  "1100000000000000000",          
   "close":  "1100000000000000000",          
   "low":  "1100000000000000000",            
   "high": "1100000000000000000",           
   "volume": "10000000000000000000"          
  }
  ````


-------------------------------

<span id="push-ticker"></span>
* Push ticker info 
  * Subscribe channel: `match`
  * Maximum 1 push within 3s
  ```json
  {
   "type": "ticker",
   "tradeSeq": 20,
   "sequence": 85,
   "time": 1650958799,
   "productId": "UNI-USDC",
   "price": "90000000000",      
   "side": "sell",       
   "lastSize": "10000000",
   "bestBid": "",
   "bestAsk": "",
   "volume24h": "110000000000000000", 
   "volume30d": "310000000000000000", 
   "low24h": "1000000000000000",     
   "high24h": "1000000000000000",    
   "open24h": "1000000000000000",
   "close24h": "1000000000000000"    
  }
  ```
-------------------------------

<span id="push-match"></span>
* Push matching info
   * Subscribe channel: `match`
   * Since the settlement of ZKEX is in Layer 2, `match` only means that the matching is successful, not that the transaction is successful
  ```json
  {
   "type": "match",
   "tradeSeq": 20,
   "sequence": 100,
   "time": 1650958799,
   "productId": "UNI-USDC",
   "price": "900000000000",
   "size": "1000000000",
   "makerOrderId": "45",     # maker's order id
   "takerOrderId": "51",     # taker's order id
   "side": "sell"
  }
  ```
  
-------------------------------

<span id="push-trade"></span>
* Push trading info 
   * Subscribe channel: `trade`
   * After the `match` channel is pushed, if layer2 is actually done, the `trade` channel will be pushed.
  ```json
  {
   "type": "trade",
   "tradeSeq": 20,
   "time": 1650958799,
   "productId": "UNI-USDC",
   "price": "900000000000",
   "size": "1000000000",
   "makerOrderId": "45",     # maker's order id
   "takerOrderId": "51",     # taker's order id
   "side": "sell",
   "status": 2
  }
  ```
-------------------------------

<span id="push-order"></span>
* Push order change infomation of a trading pair
   * Subscribe channel: `order`
   
  ```json
  {
   "userId": 1,
   "type": "order",
   "sequence": 0,
   "id": "50",
   "price": "1000000000",
   "size": "1000000000000",
   "funds": "0",
   "productId": "UNI-USDC",
   "side": "sell",
   "orderType": "limit", 
   "createdAt": 1650958799,
   "fillFees": "0",         # fee (calculated in quote tokens)
   "filledSize": "0",       # number of successfully matched (calculated in base tokens)
   "executedValue": "0",     # value of successfully matched (calculated in quote tokens)
   "status": "new",      # order status:   `new`, `open`, `filled`, `cancelled`, `cancelling` 
   "settled": false,     # whether the matching was successful
   "timeInForce": "GTC"     
  }
  ```
-------------------------------

<span id="push-funds"></span>
* Push the asset change infomation of an account
   * Subscribe channel: `funds`
   
  ```json
  {
   "type": "funds",
   "sequence": 0,
   "userId": "1",
   "currencyCode": "UNI",
   "available": "820900000000000000", 
   "hold": "11741000000000000000"  
  }
  ```
 