# Apit212

This is a Pyhton based API using selenium and requests. 

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

## Usage

### Get ask price

This line of code will return the current ask price as a float.

```ask_price = client.get_ask("TSLA")[0]['response']['price']```

#### 

## Disclaimer

This is an unofficial API & either myself of trading212 are responsible for the use of this API. It is strongly advised that you use a practice account before moving onto real money.
