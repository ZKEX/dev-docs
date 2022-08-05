
<p align="center"><img width="100%" src="https://github.com/ZKEX/dev-docs/blob/1bc6163499765d09ba188ecdf64f7aae3f2db149/zkex-banner.jpg" alt="zkex matching structure"></p>

ZKEX is a decentralized L2 multi-chain order book exchange (DEX), build on three ZK-rollups: `zkLink`, `Starkware`, and `zkSync`.

Users will be able to trade assets from multiple chains with a similar experience as on Binance or Coinbase, but instead, ZKEX will be decentralized, trust minimized, and non-custodial, with transactions secured with zero-knowledge proofs.


<summary>Table of Contents</summary>

- [Getting Started](#getting-started)
- [The difference between common users and market makers](#the-difference-between-common-users-and-market-makers)
- [ZKEX Matching Engine structure](#zkex-matching-engine-structure)
- [How to become a market maker](#how-to-become-a-market-maker)
- [Market Maker API](#market-maker-api)
  - [REST Interface (Recommend)](https://github.com/ZKEX/dev-docs/tree/main/market-maker-apis#rest-interface-recommend)
  - [REST Interface (Like binance api)](https://github.com/ZKEX/dev-docs/tree/main/market-maker-apis#rest-interface-like-binance-api)
  - [Websocket Subscribe & Cancel](https://github.com/ZKEX/dev-docs/tree/main/market-maker-apis#websocket-subscribe--cancel)
  - [Websocket Data Push](https://github.com/ZKEX/dev-docs/tree/main/market-maker-apis#websocket-data-push)

## Getting Started

Currently, ZKEX supports two ways to access: 

* `regular mode` for common users
  - zkex front-end pages
    - [devnet.app.zkex.com](https://devnet.app.zkex.com)
    - [app.zkex.com(#TODO)](#)
  - regular-mode-api (#TODO)
* `market maker mode` for market maker
  - [Market Maker API](#market-maker-api)
    

Regular mode users include:
zkex front-end users
Users connected through orderbook-apis
Market maker mode users include:
Users connected through market-maker-apis

## The difference between common users and market makers


|                                           	| Common Users                                    	| Market Makers                                                                                                                                        	|
|-------------------------------------------	|------------------------------------------	|------------------------------------------------------------------------------------------------------------------------------------------------------	|
| **Is free permission**                        	| Yes                                      	| No, apply to ZKEX Team                                                                                                                               	|
| **The way of place orders**                   	| Sign first, and submit to ZKEX Matching. 	| Place an order without signature. <br>After the match is successful, <br>zkex matching will send a request to <br>market maker to get the signature. 	|
| **Limit on the number of pending orders**     	| Less than or equal to `16`                 	| Unlimit                                                                                                                                              	|
| **Order frequency**                           	| less than `3` per second                   	| less than `30` per second                                                                                                                              	|
| **Whether there is a partially filled order** 	| Yes.                                     	| No. Because the market maker's order is <br>first matched and then signed, <br>so there is no partial filled order.                                  	|

## ZKEX Matching Engine structure
<p align="center"><img width="100%" src="https://github.com/ZKEX/dev-docs/blob/04ea4fc2e239bf29a495ed464ba338cc75b5673e/tech.png" alt="zkex matching structure"></p>

## How to become a market maker

* step1: read [FAQ docs](https://github.com/ZKEX/dev-docs/tree/main/faq)
* step2: read [market make api docs](https://github.com/ZKEX/dev-docs/tree/main/market-maker-apis#getting-started)
* step3: apply to ZKEX Team for `api key` & `api secret` (Send your basic infomation to dev@zkex.com)
* step4: clone [market-maker-signer-service](https://github.com/ZKEX/market-maker-signer-service) (This is a private repo)
* step5: initial your account. (deposit and active)
* step6: get token from faucet. (if testnet)


## Market Maker API

1. [Getting Started](https://github.com/ZKEX/dev-docs/tree/main/market-maker-apis#getting-started)

2. [REST Interface (Recommend)](https://github.com/ZKEX/dev-docs/tree/main/market-maker-apis#rest-interface-recommend)

3. [REST Interface (Like binance api)](https://github.com/ZKEX/dev-docs/tree/main/market-maker-apis#rest-interface-like-binance-api)

4. [Websocket Subscribe & Unsubscribe](https://github.com/ZKEX/dev-docs/tree/main/market-maker-apis#websocket-subscribe--unsubscribe)

5. [Websocket Data Push](https://github.com/ZKEX/dev-docs/tree/main/market-maker-apis#websocket-data-push)

