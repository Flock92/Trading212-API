# Apit212

This is a Pyhton based API using selenium and requests to get insformation from the broker trading 212. Please note that either myself or trading212 take responsibility for the use of this API.

## Requirments

* Selenium
* Requests
* Python3
* Firefox

## Installation

pip install apit212

## Import

### Demo account: 

```py

from apit212 import *

Client = Apit212(username="flock92@account.api", password="pass******", mode="demo")

````

### Live account:

```py

from apit212 import *

Client = Apit212(username="flock92@account.api", password="pass******", mode="live")

````

---

## Usage

### Get Ask Price

This line of code will return the current ask price as a float.

```py

ask_price = client.get_ask("TSLA")[0]['response']['price']

print(ask_price)

```

### Get Companies

The get companies function will return companies currently listed on T212 & their respective isin ID.

```py

companies = client.get_companies()

print(companies)

```

### Get Account

The get account function will return your account details.

```py

account = client.get_account()

print(account)

```

#### Example:

```

{'demoAccounts': [{'id': ********, 'type': 'DEMO', 'tradingType': 'CFD', 'customerId': ********,
'createdDate': '2023-01-17T03:20:48.000+00:00', 'status': 'ACTIVE', 'registerSource': 'WC4',
'currencyCode': 'GBP', 'readyToTrade': True}], 'liveAccounts': [{'id': ********, 'type': 'LIVE',
'tradingType': 'CFD', 'customerId': ********, 'createdDate': '2023-01-17T03:20:32.000+00:00',
'status': 'PENDING_ACTIVATION', 'registerSource': 'WC4', 'currencyCode': 'GBP', 'readyToTrade': False}]}

```


### Get Funds

The get funds function will return your accounts funds.

```py

funds = client.get_funds()

print(funds)

```

#### Example:

```

{'20434246': {'accountId': ********, 'tradingType': 'CFD', 'currency': 'GBP',
'freeForWithdraw': 486.83, 'freeForCfdTransfer': 0, 'total': 486.83,
'lockedCash': {'totalLockedCash': 0, 'lockedCash': []}}}

```


### Get Insturments info

The get_instrument function will retunr information about the instrument. 

```py

tsla_info = get_instruments_info('TSLA')

print(tsla_info)

```

#### Example:

```
{'code': 'TSLA', 'type': 'STOCK', 'margin': 0.2, 'shortPositionSwap': -0.07030593058663,
'longPositionSwap': -0.27928156941337, 'tsSwapCharges': '1970-01-01T23:00:00.000+02:00',
'marginPercent': '20', 'leverage': '1:5'}

```

### Get Summary

The get_summary function will return the account summary. this function can also be used to get order ID's and there current PPL

```py

summary = client.get_summary()

print(summary)

```

#### Example:

```
'open': {'unfilteredCount': 1, 'items': [{'positionId': 'd50167f2-8e03-4313-afb3-555639fe89e1', 'humanId': '3036970422',
'created': '2023-07-03T18:17:46.563+03:00', 'averagePrice': 192.25, 'averagePriceConverted': 150.73025341182984,
'currentPrice': 192.2, 'value': 1054.82, 'investment': 1055.11, 'code': 'AAPL', 'margin': 212.02, 'ppl': -0.28,
'quantity': 7, 'maxBuy': 9.0, 'maxSell': 7, 'maxOpenBuy': 2033.0, 'maxOpenSell': 2040.0, 'swap': -1.06, 'frontend': 'WC4'}]}

```

### Limit Order

```py

limit_order = client.limit_order(instrument="TSLA",
quantity=5, target_price=129, take_profit=130, stop_loss=128)

print(limit_order)

```

#### Example:

```

{'account': {'dealer': 'AVUSUK', 'positions': [{'positionId': '********-****-****-****-************',
'humanId': '**********', 'created': '2023-07-03T18:17:46.563+03:00' ...

```


## Disclaimer

This is an unofficial API & either myself of trading212 are responsible for the use of this API. It is strongly advised that you use a practice account before moving onto real money.
