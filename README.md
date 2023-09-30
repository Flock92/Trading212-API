# **Apit212**
 
This is a Pyhton based API using selenium and requests to get information from the trading212 Platform, please note that either myself or trading212 take responsibility for the outcomes related to the uses of this API.

I will continue to work on this project and would appriciate any feedback. 

## Requirments
* Selenium
* Requests
* Python3
* Firefox

## Installation

pip install apit212

## Import

to start using this API you will first need to login to the account using **apit212** you will then be able to use all the functions and create your own trading bot or use it to scarpe data from the trading212 platform.

### Demo account: 

```py

from apit212 import *

api = Apit212()

api.setup(username="flock92@account.api", password="pass******", mode="demo")

```

### Live account:

```py

from apit212 import *

api = Apit212()

api.setup(username="flock92@account.api", password="pass******", mode="live")

```

### Best Practice

It's good practice to set up an env file to save sensitive informaton like your user name or password. *Here is a useful link* [.env](https://pypi.org/project/python-dotenv/)

```env

USER=flock92@account.api
PASS=password123

```

```py

from dotenv import load_dotenv
from apit212 import *
import os

load_dotenv('.env')

username: str = os.getenv('USER')
password: str = os.getenv('PASS')

api = Apit212()

api.setup(username="flock92@account.api", password="pass******", mode="demo")

```
---

# CFD or Trade Equity

To trade CFD's simply call the CFD class

```py

from apit212 import *

api = Apit212()

api.setup(username="flock92@account.api", password="pass******", mode="demo")

cfd = CFD(cred=api)

```

To trade Equity's simply call the Equity class.

```py

from apit212 import *

client = Apit212(username="flock92@account.api", password="pass******", mode="live")

equity = Equity()

```


## Account data

### Check session

The *auth_validate* function will return account ID and trade type.

```py

validate = cfd.auth_validate()

print(validate)

```

#### Console:

```bash

{'id': '*******-****-****-****-************', 'accountId': ********, 'customerId': *********, 'tradingType': 'CFD', 'customerUuid': '********-****-****-****-************', 'frontend': 'WC4', 'readyToTrade': True, 'deviceUuid': ''}

```

### get_account

The *get_account* function will return your account details.

```py

account = cfd.get_account()

print(account)

```

#### Console

```bash

{'demoAccounts': [{'id': ********, 'type': 'DEMO', 'tradingType': 'CFD', 'customerId': ********,
'createdDate': '2023-01-17T03:20:48.000+00:00', 'status': 'ACTIVE', 'registerSource': 'WC4',
'currencyCode': 'GBP', 'readyToTrade': True}], 'liveAccounts': [{'id': ********, 'type': 'LIVE',
'tradingType': 'CFD', 'customerId': ********, 'createdDate': '2023-01-17T03:20:32.000+00:00',
'status': 'PENDING_ACTIVATION', 'registerSource': 'WC4', 'currencyCode': 'GBP', 'readyToTrade': False}]}

```

### get_funds

The *get_funds* function will return the accounts funds.

```py

funds = cfd.get_funds()

print(funds)

```

#### Console

```bash

{'*******': {'accountId': ********, 'tradingType': 'CFD', 'currency': 'GBP',
'freeForWithdraw': 486.83, 'freeForCfdTransfer': 0, 'total': 486.83,
'lockedCash': {'totalLockedCash': 0, 'lockedCash': []}}}

```

### Get summary

The *get_summary* returns a summary of you account.

```py

summary = cfd.get_summary()

print(summary)

```

#### Console

```bash

'open': {'unfilteredCount': 1, 'items': [{'positionId': '********-****-****-****-************', 'humanId': '********',
'created': '2023-07-03T18:17:46.563+03:00', 'averagePrice': 192.25, 'averagePriceConverted': 150.73025341182984,
'currentPrice': 192.2, 'value': 1054.82, 'investment': 1055.11, 'code': 'AAPL', 'margin': 212.02, 'ppl': -0.28,
'quantity': 7, 'maxBuy': 9.0, 'maxSell': 7, 'maxOpenBuy': 2033.0, 'maxOpenSell': 2040.0, 'swap': -1.06, 'frontend': 'WC4'}]}

```

### Get companies

The *get_companies* returns instruments avaliable to trade on the trading212 platform

```py

companies = cfd.get_companies()

print(companies)

```

#### Console

```bash

[{'ticker': 'SIGTl_EQ', 'isin': 'GB0008769993'}, {'ticker': 'PDYPY_US_EQ', 'isin': 'US3440441026'}...]

```

### Get instrument info

The *get_instruments_info* will return information about an instrument.

```py

info = cfd.get_instruments_info(instrument="TSLA")

print(info)

```

#### Console

```bash

{'code': 'TSLA', 'type': 'STOCK', 'margin': 0.2, 'shortPositionSwap': -0.07030593058663,
'longPositionSwap': -0.27928156941337, 'tsSwapCharges': '1970-01-01T23:00:00.000+02:00',
'marginPercent': '20', 'leverage': '1:5'}

```

### Get order info

The *get_order_info* get 

```py

orderInfo = cfd.get_order_info(instrument="TSLA", quamtity=1.5)

print(orderInfo)

```

#### Console

```bash

{'buyMargin': 40.18, 'sellMargin': 40.18, 'buySwap': -0.2, 'sellSwap': -0.05}

```

### Get deviation

```py

tickers = ["TSLA","AAPL"]

deviation = cfd.get_deviations(instruments=tickers)

print(deviation)

```

#### Console

```bash

[{'request': {'ticker': 'TSLA', 'useAskPrice': False}, 'response': {'timestamp': 1694073610000, 'price': 250.68, 'period': 'd1'}}, {'request': {'ticker': 'AAPL', 'useAskPrice': False}, 'response': {'timestamp': 1694073610000, 'price': 178.18, 'period': 'd1'}}]

```

### Get position

The *get_position* returns infomation for a given position ID, this ID's can be exstracted from the get_summary function

```py

position = cfd.get_position(position_id=274187113)

print(position)

```

#### Console

```bash

[{'eventType': {'action': 'opened', 'source': 'MARKET_ORDER'}, 
'eventNumber': {'name': 'MO3053019640', 'id': '274187113', 'frontend': 'WC4'}, 'time': '2023-08-02T22:42:54.000+03:00', 
'direction': 'sell', 'quantity': 1.0, 'price': '105.29', 'avgQuantity': 1.0, 'avgPrice': '105.2900', 'modifiedDirection': 
'sell'}]

```

### Get all results

The *get_all_result* function will return a list of all your trading results. you will need to request each page. you may also need to pass your timezone.

```py

results = cfd.get_all_results()

print(results)

```

#### Console

```bash

{'data': [{'direction': 'buy', 'code': 'AAPL', 'quantity': 0.1, 'orderNumber': {'name': 'P************', 'link': 'positionHistory/********-****-****-****-************', 'id': '********-****-****-****-************', 'frontend': 'WC4'}, 'price': '176.6700', 'closePrice': '181.98', 'result': '0.42', 'eventNumber': {'name': 'PO3062546222', 'id': '********-****-****-****-************'}, 'eventType': 'closed', 'time': '2023-08-29T17:15:55.000+03:00', 'openingTime': '2023-08-25T11:51:15.000+03:00'}, ...], 'nextPage': 'result?perPage=20&onlyFullyClosed=false&page=2', 'currentPage': 'result?perPage=20&onlyFullyClosed=false&page=1', 'totalSize': 133}

```

### Get order History

```py

orderHist = cfd.get_order_hist(page_number=1)

print(orderHist)

```

#### Console

```bash

{'data': [], 'currentPage': 'order?filter=all&perPage=20&from=2023-09-06T02:00:00.000+03:00&to=2023-09-08T01:59:59.173+03:00&page=1', 'totalSize': 0}

```

### Get position History

```py

positionHist = cfd.get_posistion_hist(page_number=1)

print(positionHist)

```

#### Console

```bash

{'data': [], 'currentPage': 'position?perPage=20&from=2023-09-06T02:00:00.000+03:00&to=2023-09-08T01:59:59.173+03:00&page=1', 'totalSize': 0}

```

### fast price

The *fast_price* retruns an instruments price as a float. if the request fails None is returned

```py

price = cfd.fast_price(instrument="TSLA")

print(price)

```

#### console

```bash

253.49

```

### Chart data

The *chart_data* returns a dictionary with the candle date OHLC (open, high, low, close) the period requested. which is set to 1minute by default.

```py

charts = cfd.chart_data(instrument="TSLA", period="ONE_MINUTE")

print(charts)

```

#### Console

```bash

[{'request': {'ticker': 'TSLA', 'period': 'ONE_MINUTE', 'size': 500, 'useAskPrice': False}, 'response': {'candles': [[1691152740000, 259.6, 259.97, 259.43, 259.49, 47], [1691152800000, 259.38, 259.94, 259.17, 259.56, 58], [1691152860000, 259.62, 260.34, 259.62, 260.19, 42]

```

### Get multiple price data

The *multi_price* function will return the last qouted price for all passed instruments.

```py

tickers =["TSLA","AAPL","GOOG"]

multiprice = cfd.multi_price(instruments=tickers)

print(multiprice)

```

#### Console

```bash

[{'ticker': 'TSLA', 'price': 251.34}, {'ticker': 'AAPL', 'price': 181.96}, {'ticker': 'GOOG', 'price': 135.18}]

```

## TRADES

### Market order

The *market_order* function submits a market order and requires the current price of the instrument.

```py

targetPrice = cfd.fast_price(instrument="TSLA")

marketOrder = cfd.market_order(instrument="TSLA", target_price=targePrice,
quantity=1.5, take_profit=10, stop_loss=10 )

```

### Limit order

The *limit_order* function submits a limit order

```py

marketOrder = cfd.limit_order(instrument="TSLA", target_price=127,
quantity=1.5, take_profit=10, stop_loss=10)

```

### Set limits

The *set_limits* function allows you to modify or add a stoploss or takeprofit to an existing postion (the positionID is required to carry out this function)

```py

limits = cfd.set_limits(position_id=27361748, TP=10, SL=10)

```

### add trailing stop

The *add_trailing_stop* function adds a trailing stop to an existing position

```py

trailing = cfd.add_trailing_stop(position_id=27361748, distance=1)

```

### close position

The *close_position* function is used to close an open position. it will required the current price.

```py

currentPrice = cfd.fast_price(instrument="TSLA")

close = cfd.close_position(position_id=23948174, current_price=currentPrice)

```

### cancel all orders

```py

cancelAll = cfd.cancel_all_orders()

```

### cancel order

The *cancel_order* function is used to cancel a limit order.

```py

cancel = cfd.cancel_order(order_id=**********)

```



### Get ticker price

the *get_live* function will return the current price of a ticker

```py

tickers = ["TSLA", "AAPL"]

prices = cfd.live_price(instruments=tickers)

print(prices)

```

#### Console:

```bash

[{'request': {'ticker': 'TSLA', 'useAskPrice': False}, 'response': {'timestamp': 1690531210000, 'price': 255.8, 'period': 'd1'}}, {'request': {'ticker': 'AAPL', 'useAskPrice': False}, 'response': {'timestamp': 1690531210000, 'price': 193.29, 'period': 'd1'}}]

```

### Get Funds

The *get_funds* function will return your accounts funds.

```py

funds = cfd.get_funds()

print(funds)

```

#### Console:

```bash

{'20434246': {'accountId': ********, 'tradingType': 'CFD', 'currency': 'GBP',
'freeForWithdraw': 486.83, 'freeForCfdTransfer': 0, 'total': 486.83,
'lockedCash': {'totalLockedCash': 0, 'lockedCash': []}}}

```

### Add trailing stop loss

the *trailing_stop* function allows you to add a trailing stop to a open position.

```py

trailing_stop = cfd.trailing_stop(position_id="***-****-***", distance=0.5)

```

### Add/Change stoploss and takeprofit

The *add_limits* function allows you to add a stoploss and takeprofit to an existing position.

```py

update_limits = client.add_limits(position_id="***-****-***", TP=1 , SL=1)

```
To set a new stoploss or takeprofit just pass the distance to the TP (take profit) or SL (stop loss) params. The function will get the current price and apply the distance.

### Get all position history

The *all_position_hist* function will return the position history.

```py

position_history = cfd.all_position_hist()

```

### Get order history

The *all_order_hist* returns orders data

```py

order_history = cfd.all_order_hist()

```

### Get Insturments info

The *get_instrument* function will retunr information about the instrument. 

```py

tsla_info = cfd.get_instruments_info(instrument='TSLA')

print(tsla_info)

```

#### Console:

```bash

{'code': 'TSLA', 'type': 'STOCK', 'margin': 0.2, 'shortPositionSwap': -0.07030593058663,
'longPositionSwap': -0.27928156941337, 'tsSwapCharges': '1970-01-01T23:00:00.000+02:00',
'marginPercent': '20', 'leverage': '1:5'}

```

### Get position information

The *get_position* function will returns information for the qouted positionID.

```py

position = cfd.get_position(position_id="***-****-***")

print(position)

```

#### console

```bash

[{'eventType': {'action': 'opened', 'source': 'MARKET_ORDER'}, 
'eventNumber': {'name': 'MO3053019640', 'id': '274187113', 'frontend': 'WC4'}, 'time': '2023-08-02T22:42:54.000+03:00', 
'direction': 'sell', 'quantity': 1.0, 'price': '105.29', 'avgQuantity': 1.0, 'avgPrice': '105.2900', 'modifiedDirection': 
'sell'}]

```

### Get Summary

The *get_summary* function will return the account summary. this function can also be used to get order ID's and there current PPL

```py

summary = cfd.get_summary()

print(summary)

```

#### Example:

```bash
'open': {'unfilteredCount': 1, 'items': [{'positionId': '********-****-****-****-************', 'humanId': '********',
'created': '2023-07-03T18:17:46.563+03:00', 'averagePrice': 192.25, 'averagePriceConverted': 150.73025341182984,
'currentPrice': 192.2, 'value': 1054.82, 'investment': 1055.11, 'code': 'AAPL', 'margin': 212.02, 'ppl': -0.28,
'quantity': 7, 'maxBuy': 9.0, 'maxSell': 7, 'maxOpenBuy': 2033.0, 'maxOpenSell': 2040.0, 'swap': -1.06, 'frontend': 'WC4'}]}

```

### Get live Price

The *live_price* function will return the current ask price for the passed instrument.

```py

ticker = ["TSLA","AAPL","GOOG"]

live_price = cfd.live_price(instruments=ticker)

print(live_price)


```

#### console:

```bash

[{'ticker': 'TSLA', 'price': 253.49}, {'ticker': 'AAPL', 'price': 182.08}, {'ticker': 'GOOG', 'price': 128.44}]


```

### Get fast price

The *fast_price* function will return the last qouted chart price as a float

```py

price = cfd.fast_price(instrument="TSLA")

print(price)


```

#### console:

```bash

253.49

```

### Get chart data

the *chart_data* function will return the lastest chart data for passed instrument

```py

chart = cfd.chart_data(instrument="TSLA")

print(chart)

```

#### console:

```bash

[{'request': {'ticker': 'TSLA', 'period': 'ONE_MINUTE', 'size': 500, 'useAskPrice': False}, 'response': {'candles': [[1691152740000, 259.6, 259.97, 259.43, 259.49, 47], [1691152800000, 259.38, 259.94, 259.17, 259.56, 58], [1691152860000, 259.62, 260.34, 259.62, 260.19, 42]

```

### Get price deviations

The *get_deviations* function will return price deviations

```py

ticker = ["TSLA","AAPL","GOOG"]

deviations = cfd.get_deviations(instruments=ticker)

print(deviations)

```

#### console:

```bash

[{'request': {'ticker': 'TSLA', 'useAskPrice': False}, 'response': {'timestamp': 1691136010000, 'price': 259.38, 'period': 'd1'}}, {'request': {'ticker': 'AAPL', 'useAskPrice': False}, 'response': {'timestamp': 1691136010000, 'price': 188.99, 'period': 'd1'}}, {'request': {'ticker': 'GOOG', 'useAskPrice': False}, 'response': {'timestamp': 1691136010000, 'price': 129.05, 'period': 'd1'}}]

```

### Get Companies

The *get_companies* function will return companies currently listed on T212 & their respective isin ID.


```py


companies = cfd.get_companies()

print(companies)


```

#### console:

```bash

[{'ticker': 'SIGTl_EQ', 'isin': 'GB0008769993'}, {'ticker': 'PDYPY_US_EQ', 'isin': 'US3440441026'}...]

```

### Limit Order

The *limit_order* function submit a limit order and takes quantity, target_price, take_profit & stop_loss parms.

```py

limit_order = cfd.limit_order(instrument="TSLA",
quantity=5, target_price=129, take_profit=130, stop_loss=128)

```

#### Console:

```

{'account': {'dealer': 'AVUSUK', 'positions': [{'positionId': '********-****-****-****-************',
'humanId': '**********', 'created': '2023-07-03T18:17:46.563+03:00' ...

```

### Market Order
The *market_order* function submit a market order and takes quantity, target_price, take_profit & stop_loss parms.

```py

market_order = cfd.market_order(instrument="TSLA",
quantity=5, target_price=129, take_profit=130, stop_loss=128)


```

### Cancel order
The *cancel_order* function will cancel a pending order it requires a orderID.

```py

cancel_order = cfd.cancel_order(order_id)


```

You can also use the *cancel_all_orders* to cancel all pending limits orders.


```py

cancel_all = cfd.cancel_all_orders()

```

### Close Position
The *close_position* function will submit a request to cancel a open position.

```py


close_position = cfd.close_position(position_id=market_order, quantity=market_order, current_price=current_price)


```

## CODE EXAMPLES


```py

username = "flock92@account.api"
password = "password132"

api = Apit212()

api.setup(username=username, password=password, mode="demo")

cfd = CFD(cred=api)

target_price = 128

while True:

    sleep(60)

    price = cfd.fast_price("TSLA")

    if price <= target_price:

        marketOrder = cfd.market_order(instrument="TSLA",           target_price=price, quantity=1, take_profit=10, 
        stop_loss=10)

        break

```

# Trade Exceptions

When carrying out a trade you might run into issues and it's always good to have protocols in place to deal with these issues when they arise.

below is a list of **some** exceptions you might come across when carrying out a trade.

## BusinessException

* MinQuantityExceeded
* NoPriceException
* InstrumentNotSupported
* SpreadIsBiggerThanMinDistance
* InstrumentDisabled
* StopLossMustBeBelowCurrentPrice
* InsufficientFundsMaxBuy
* InsufficientFundsMaxSell
* MarketStillNotOpen
* QuantityPrecisionMismatch

## InternalError

Just stop making the request if you get this response

# Using trading212 official API

This is currently only working with equity accounts and you can only submit trades on your demo account. please read the official documentation to get a better understanding and limitations of the API.

## Setup

In order to use the official API you will need to generate a key using the trading212 app. /settings/API(Beta) then simply generate a new Key and pass it to the *Apitkey().Equity()* Class.

```py

from apit212 import *

key = "20557******************************"

client = Apitkey()

info = client.Equity(api_key=key, mode="live")

```

### Functions

Here are the functions avalible using the trading212 API-token.

* [exchange_list](https://t212public-api-docs.redoc.ly/#operation/exchanges)
* [instrument_list](https://t212public-api-docs.redoc.ly/#operation/instruments)
* [pies](https://t212public-api-docs.redoc.ly/#tag/Pies)
* [create_pie](https://t212public-api-docs.redoc.ly/#operation/create)
* [delete_pie](https://t212public-api-docs.redoc.ly/#operation/delete)
* [fetch_pie](https://t212public-api-docs.redoc.ly/#operation/getDetailed)
* [update_pie](https://t212public-api-docs.redoc.ly/#operation/update)
* [equity_orders](https://t212public-api-docs.redoc.ly/#operation/orders) 
* [limit_order](https://t212public-api-docs.redoc.ly/#operation/placeLimitOrder)
* [market_order](https://t212public-api-docs.redoc.ly/#operation/placeMarketOrder) 
* [stop_oder](https://t212public-api-docs.redoc.ly/#operation/placeStopOrder_1) 
* [stop_limit_order](https://t212public-api-docs.redoc.ly/#operation/placeStopOrder) 
* [cancel_order](https://t212public-api-docs.redoc.ly/#operation/cancelOrder)
* [fetch_order](https://t212public-api-docs.redoc.ly/#operation/orderById)
* [account_data](https://t212public-api-docs.redoc.ly/#operation/accountCash)
* [account_meta](https://t212public-api-docs.redoc.ly/#operation/account)
* [fetch_all_posistions](https://t212public-api-docs.redoc.ly/#operation/portfolio)
* [fetch_position](https://t212public-api-docs.redoc.ly/#operation/positionByTicker)
* [order_history](https://t212public-api-docs.redoc.ly/#operation/orders_1)
* [paid_out_dividends](https://t212public-api-docs.redoc.ly/#operation/dividends)
* [export_list](https://t212public-api-docs.redoc.ly/#operation/getReports)
* [export_csv](https://t212public-api-docs.redoc.ly/#operation/requestReport)
* [transactions](https://t212public-api-docs.redoc.ly/#operation/transactions)

# Disclaimer

This is an unofficial API & either myself of trading212 are responsible for the use of this API. It is strongly advised that you use a practice account before moving onto real money. *apit212 is **not** a trading bot*

