# **Apit212**

This is a Pyhton based API using selenium and requests to get insformation from the broker trading 212 Please note that either myself or trading212 take responsibility for the use of this API.
I will continue to work on this project and would appriciate any feedback. 

[link](https://t212public-api-docs.redoc.ly/#operation/exchanges)]

## Requirments

* Selenium
* Requests
* Python3
* Firefox

## Installation

pip install apit212

## Import

to start using this API you will first need to login to the account using **apit212** you will then be able to use all the functions and create your own trading bot.

### Demo account: 

```py

from apit212 import *

client = Apit212(username="flock92@account.api", password="pass******", mode="demo")

```

### Live account:

```py

from apit212 import *

client = Apit212(username="flock92@account.api", password="pass******", mode="live")

```
### Best Practice

It's good practice to set up an env file to save sensitive informaton like your user name or password. *Here is a useful link* [.env](https://pypi.org/project/python-dotenv/)

```env

USER=flock92@account.api
PASS=password

```

```py

from dotenv import load_dotenv
import os

load_dotenv('.env')

username: str = os.getenv('USER')
password: str = os.getenv('PASS')

client = Apit212(username=username, password=password, mode="demo")

```
---

## Usage

### Get Account

The *get_account* function will return your account details.

```py

account = client.get_account()

print(account)

```

#### Console:

```bash

{'demoAccounts': [{'id': ********, 'type': 'DEMO', 'tradingType': 'CFD', 'customerId': ********,
'createdDate': '2023-01-17T03:20:48.000+00:00', 'status': 'ACTIVE', 'registerSource': 'WC4',
'currencyCode': 'GBP', 'readyToTrade': True}], 'liveAccounts': [{'id': ********, 'type': 'LIVE',
'tradingType': 'CFD', 'customerId': ********, 'createdDate': '2023-01-17T03:20:32.000+00:00',
'status': 'PENDING_ACTIVATION', 'registerSource': 'WC4', 'currencyCode': 'GBP', 'readyToTrade': False}]}

```

### Get ticker price

the *get_live* function will return the current price of a ticker

```py

tickers = ["TSLA", "AAPL"]

prices = client.live_price(instruments=tickers)

print(prices)

```

#### Console:

```bash

[{'request': {'ticker': 'TSLA', 'useAskPrice': False}, 'response': {'timestamp': 1690531210000, 'price': 255.8, 'period': 'd1'}}, {'request': {'ticker': 'AAPL', 'useAskPrice': False}, 'response': {'timestamp': 1690531210000, 'price': 193.29, 'period': 'd1'}}]

```

### Get Funds

The *get_funds* function will return your accounts funds.

```py

funds = client.get_funds()

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

trailing_stop = client.trailing_stop(position_id="***-****-***", distance=0.5)

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

position_history = client.all_position_hist()

```

### Get order history

The *all_order_hist* returns orders data

```py

order_history = client.all_order_hist()

```

### Get Insturments info

The *get_instrument* function will retunr information about the instrument. 

```py

tsla_info = client.get_instruments_info(instrument='TSLA')

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

position = client.get_position(position_id="***-****-***")

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

summary = client.get_summary()

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

live_price = client.live_price(instruments=ticker)

print(live_price)


```

#### console:

```bash

[{'ticker': 'TSLA', 'price': 253.49}, {'ticker': 'AAPL', 'price': 182.08}, {'ticker': 'GOOG', 'price': 128.44}]


```

### Get fast price

The *fast_price* function will return the last qouted chart price as a float

```py

price = client.fast_price(instrument="TSLA")

print(price)


```

#### console:

```bash

253.49

```

### Get chart data

the *chart_data* function will return the lastest chart data for passed instrument

```py

chart = client.chart_data(instrument="TSLA")

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

deviations = client.get_deviations(instruments=ticker)

print(deviations)

```

#### console:

```bash

[{'request': {'ticker': 'TSLA', 'useAskPrice': False}, 'response': {'timestamp': 1691136010000, 'price': 259.38, 'period': 'd1'}}, {'request': {'ticker': 'AAPL', 'useAskPrice': False}, 'response': {'timestamp': 1691136010000, 'price': 188.99, 'period': 'd1'}}, {'request': {'ticker': 'GOOG', 'useAskPrice': False}, 'response': {'timestamp': 1691136010000, 'price': 129.05, 'period': 'd1'}}]

```

### Get Companies

The *get_companies* function will return companies currently listed on T212 & their respective isin ID.


```py


companies = client.get_companies()

print(companies)


```

#### console:

```bash

[{'ticker': 'SIGTl_EQ', 'isin': 'GB0008769993'}, {'ticker': 'PDYPY_US_EQ', 'isin': 'US3440441026'}...]

```

### Limit Order
The *limit_order* function submit a limit order and takes quantity, target_price, take_profit & stop_loss parms.

```py

limit_order = client.limit_order(instrument="TSLA",
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

market_order = client.market_order(instrument="TSLA",
quantity=5, target_price=129, take_profit=130, stop_loss=128)


```

### Cancel order
The *cancel_order* function will cancel a pending order it requires a orderID.

```py

cancel_order = client.cancel_order(order_id)


```

You can also use the *cancel_all_orders* to cancel all pending limits orders.


```py

cancel_all = client.cancel_all_orders()

```

### Close Position
The *cancel_position* function will submit a request to cancel a open position.

```py


cancel_position = client.close_position(position_id=market_order, quantity=market_order, current_price=current_price)


```

### headers
In apit212 you can save the headers which would allow you to run a request without the need to run through the login proccess. But this won't last forevery the session with T212 will Timeout.

```py


client = Apit212(username="flock92@account.api", password="pass******", mode="live")

headers = client.headers

print(headers)


```
Once you've saved your cookies you bypass the login stage by passing it to the header params as a dict.

```py


headers = {'Accept': 'application/json',
           'Content-Type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0',
           'Cookie': 'TRADING212_SESSION_DEMO=***********;'}

client = Apit212(username="flock92@account.api", password="pass******", headers=headers)


```

## CODE EXAMPLES

Code below will add a stoploss and takeprofit to an existing position

```py

summary = client.get_summary()

for items in enumerate(summary["open"]["items"])
    positionID = items[i[0]]["positionId"]

```

## Disclaimer

This is an unofficial API & either myself of trading212 are responsible for the use of this API. It is strongly advised that you use a practice account before moving onto real money. *apit212 is **not** a trading bot*

