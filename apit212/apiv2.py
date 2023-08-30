# this unofficial API was created by Flock92 originally made to automate my CFD trading on the trading212 platform
# https://www.youtube.com/watch?v=_YVQN6_nkfs

from typing import Any
from requests import Session
from requests import Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from requests_html import HTML
from time import sleep
import pandas as pd
from datetime import timedelta
import datetime
import requests
import json
import js2py
import os


class _Constant:

    def __init__(self) -> None:
        pass

class Apit212(_Constant):

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
               }
    
    session = Session()
    session.headers = headers

    def __init__(self) -> None:
        # retrun session values
        pass
      
    def setup(self, username: str, password: str) -> None:
        """
        """
        self.user = username # required to re-establish connection

        scriptUrl = "https://www.trading212.com/_next/static/chunks/pages/_app-fedf6306a52a9d19.js"

        self.url = f'https://www.trading212.com'

        # Load trading212 website

        self.url = f'https://www.trading212.com/'
        options = webdriver.FirefoxOptions()
        options.add_argument('--log-level=3')
        options.add_argument('-headless')
        d = webdriver.Firefox(options=options)
        d.get(self.url)

        # TRY USE JS TO GET STATIC KEY example 6LcUCfIdAAAAACFnE6J_5c6uUZqTRG11umc1nVgO
        #

        # Get auth token
        iframe = d.find_element(By.CSS_SELECTOR, ".grecaptcha-logo > iframe:nth-child(1)")

        link = str(iframe.get_attribute('src'))

        r = self.session.get(link)

        content = r.content

        soup = BeautifulSoup(content, "html.parser")

        print(soup)

        r = self.session.post(url=f"{self.url}/api/authentication/authenticate")
        print(r)

        quit()

        token = soup.find("input", id="recaptcha-token")["value"]

        #token = str(input).split('"')

        print(token)

        #print(soup.find("input", id="recaptcha-token")) # GET VALUE FOR LOGIN REQUEST

        # Login 
        loginUrl = "https://www.trading212.com/api/authentication/login"

        payload = {
            "username":f"{username}",
            "password":f"{password}",
            "rememberMe":"true",
            "recaptchaToken":f"{token}"
            
        }

        #print(payload)

        r = self.session.post(url=loginUrl, data=json.dumps(payload))

        #r = requests.post(url=loginUrl, headers=self.headers,
        #                 data=json.dumps(payload), timeout=(3, 22))
        #
        print(r.status_code)
        print(r.headers)

        d.close()
        d.quit()
        quit()

        # iframe title = reCAPTCHA

        my_cookie = None
        #https://www.trading212.com/api/authentication/login
        r = self.session.get(f"https://www.trading212.com")
        headers = r.headers

        for key, value in headers.items():
            self.headers.update(dict({key:value}))
            #print("[",key,"]=[",value,"]")

        # Update headers in session
        self.session.headers = self.headers

        # Make another requst
        r = self.session.get(f"https://www.trading212.com", stream=True, allow_redirects=True)
        headers = r.headers

        print(r.headers)

        page = r.text

        #print(r.content)


        # Check if headers exist

    def get_companies(self) -> list:
        """
        """

class FileHandler:

    directory = ""

    def __init__(self) -> None:
        
        if os.name == "nt":
            self.directory = "./Apit212_data/"
        else:
            self.directory = ".\\Apit212_data\\"

        # create directory if it doesnt exist
        if os.path.isdir(self.directory) == False:
            os.makedirs(self.directory)
        else:
            pass
    
    def create_file(self, filename: str, data: dict) -> None:
        """
        """
        path = f"{self.directory}{filename}.csv"

        pd.to_pickle(data, path)

    def delete_file(self, filename: str) -> None:
        """
        """
        path = f"{self.directory}{filename}.csv"

        if os.path.isfile(path) == True:
            os.remove(path)

    def read_file(self, filename: str) -> dict:
        """
        """
        path = f"{self.directory}{filename}.csv"

        if os.path.isfile(path) == True:
            data = pd.read_pickle(path)
            return dict(data)
        else:
            return {"code":"fileNotFound"}

    def update_file(self, filename: str, data: dict) -> None:
        """
        """
        path = f"{self.directory}{filename}.csv"

        if os.path.isfile(path=path) == True:
            file = self.read_file(filename=filename)
            for key, value in data.items():
                if key in file:
                    file[key] = value
                else:
                    file.__setitem__(key, value)
            
            pd.to_pickle(file, path)

        else:
            print(f"fileNotFound! : {path}")

    def check_file(self, filename: str) -> bool:
        """
        """
        path = f"{self.directory}{filename}.csv"

        return os.path.isfile(path=path) 
    
    def overwrite_file(self, filename: str, data: dict) -> None:
        """
        """
        path = f"{self.directory}{filename}.csv"

        if os.path.isfile(path=path) == True:
            file = self.read_file(filename=filename)
            file = data
            pd.to_pickle(file, path)
        else:
            self.create_file(filename=filename, data=data)

class  HandleResponse(object):

    def __init__(self, response: Response) -> None:
        """
        Handles server responses
        """

        if response.status_code == 200:
            self.return_data(data=response)

        elif response.status_code == 500:
            self.return_error(data=response)

        else:
            self.handle_exceptions(data=response)
   
    def return_data(self, data: requests.Response) -> json:
        """
        """
        return data.json()
    
    def handle_exceptions(self, data: Response) -> str:
        """
        returns message regarding server response
        """

        print(data.status_code)
        print(data.json())

    def return_error(self, data: Response) -> None:
        """
        responses to 500 errors or unknown errors and print response and 
        ends API
        """

        quit(print(data))


class CFD(Apit212):

    now = datetime.datetime.now()

    # session details required to re-establish a connection (could save to a doc)
    account = {
        "createdDate": "",
        "currencyCode": "",
        "customerId": int,
        "id": int,
        "lastSwitchedDate": "",
        "readyToTrade": bool,
        "registerSource": "",
        "status": "",
        "tradingType": "",
        "type": ""
        }

    customer = {
        "dealer": "",
        "email": "",
        "id": int,
        "lang": "",
        "registerDate": "",
        "timezone": "",
        "uuid": "",
        }

    session_info = {
        "account":account,
        "accountId": "",    # long form
        "accountSession": "",   # long form   
        "backupCode": "null",
        "customer": customer,
        "customerCookieName": "CUSTOMER_SESSION",
        "customerId": "",
        "email": "",
        "loginToken": "null",
        "rememberMeCookie":"null",
        "serverTimestamp":"",
        "subSystem":"",
        "tradingType":""
        }
    
    def __init__(self, mode: str = "demo") -> None:
        self.mode = mode 
        super().__init__("CFD")

        self.user = self.user

        self.hr = HandleResponse

        self.fh = FileHandler()

        self.url= f"https://{mode}.trading212.com"

        # switch accound


        self.s = self.session

    def switch(self, account_id: str) -> dict:
        """
        """

        payload = {"accountId": account_id}

        r = self.s.post(url=f"{self.url}/rest/v1/login/accounts/switch",
                        data=json.dumps(payload))

        return self.hr(r)

    def update_headers(self, headers: dict) -> None:
        """
        update sessions headers

        :param headers:
        """
        self.s.headers = headers

        self.fh.update_file("_cookies", headers)

    def update_session_info(self, _dealer: str = "AVUSUK", _lang: str = "EN") -> None:
        """
        get information about session to enable the 
        Apit212 to re-establish the session
        """
        filename = "_session"

        # Get account data
        accountData = self.get_account()[f"{self.mode}Accounts"]

        # Get customer data
        authData = self.auth_validate()

        # Get timezone
        timezone = self.get_timezone()

        for key, value in accountData.items():
            if key in self.account:
                self.account[key] = value

        self.customer["uuid"] = authData["customerUuid"]
        self.customer["id"] = authData["customerId"]
        self.customer["timezone"] = timezone["label"]
        self.customer["dealer"] = _dealer
        self.customer["registerDate"] = 
        self.customer["lang"] = _lang # Could get this from selenium

        # Get session data

        self.session_info["email"] = self.user
        self.session_info["accountId"] = authData["accountId"]
        self.session_info["accountSession"] = authData["id"]
        self.session_info["customerSession"] = authData["id"]
        self.session_info["customerId"] = authData["customerUuid"]
        self.session_info["type"] = accountData["type"]
        self.session_info["subSystem"] = self.mode.upper()
        self.session_info["sessionCookieName"] = f"TRADING212_SESSION_{self.mode.upper()}"

        # save to file & variable
        if self.fh.check_file(filename=filename) == True:
            self.fh.overwrite_file(filename=filename, data=self.session_info)
        else:
            self.fh.create_file(filename=filename, data=self.session_info)

    def auth_validate(self) -> dict:
        """
        get information about session
        """
        r = self.s.get(url=f"{self.url}//auth/validate")

        if r.status_code == 200:
            data = dict(r.json())
            # save values to a variable or file
            for key, value in data.items():

                pass
            self.session_info

        else:
            # attempt to re-authenticate
            self.authenticate()

    def validate_session(self) -> dict:
        """
        """
        r = self.s.get(url=f"{self.url}//auth/validate")

        self.hr(r)
 
    def authenticate(self) -> dict:
        """
        re-establish session if session has ended and update headers
        """

        # required values to re-establish connection
        """
        account : {id: 20434246, customerId: 11069497, type: "DEMO", createdDate: "2023-01-17T03:20:48.000+00:00",…}
            createdDate: "2023-01-17T03:20:48.000+00:00"        :)
            currencyCode: "GBP"                                 :)
            customerId: 11069497                                :)
            id: 20434246                                        :)
            lastSwitchedDate: "2023-08-25T10:26:59.000+00:00"   :)
            readyToTrade: true                                  :)
            registerSource: "WC4"                               :)
            status: "ACTIVE"                                    :)
            tradingType: "CFD"                                  :)
            type: "DEMO"                                        :)

        accountId : 20434246
        accountSession : "6c0d4b25-7240-4f18-a30b-f9d5a8bcd654"
        backupCode : null

        customer : {id: 11069497, uuid: "2bf01e27-3709-4579-98d2-6af6b5c9a9b2", email: "stuwe_3000@outlook.com",…}
            dealer: "AVUSUK"
            email: "stuwe_3000@outlook.com" 
            id: 11069497    :)
            lang: "EN"
            registerDate: "2023-01-17T05:20:32+02:00"
            timezone: "Europe/London"
            uuid: "2bf01e27-3709-4579-98d2-6af6b5c9a9b2" :)
        customerCookieName : "CUSTOMER_SESSION"
        customerId : "2bf01e27-3709-4579-98d2-6af6b5c9a9b2"
        customerSession : "6c0d4b25-7240-4f18-a30b-f9d5a8bcd654"
        email : "stuwe_*&&&&&&&&.com"
        loginToken : null
        rememberMeCookie : null
        serverTimestamp : "2023-08-29T16:04:47.625659532+03:00"
        sessionCookieName : "TRADING212_SESSION_DEMO" 
        subSystem : "DEMO"
        tradingType : "CFD"
        """

        payload = {

        }

        r = self.s.get(url=f"{self.url}/rest/v1/webclient/authenticate", 
                       data=json.dumps(payload))
        
        if r.status_code == 200: # if response is successful get new headers
            
            data = dict(r.json())

            for key, value in data.items():
                if key in self.headers:
                    self.headers[key] = value
                else:
                    self.headers.__setitem__(key, value)

        else:
            self.hr(r)

    def get_timezone(self) -> dict:
        """
        """

        # check "gmtLabel": "GMT +1" and get "actualZoneName": "Europe/London",
        #"label": "London, Lisbon",
        #"offset": 3600000,

        r = self.s.get(url=f"{self.url}/rest/v2/time-zones")

        return self.hr(r)
    
    def get_account(self) -> dict:
        """
        returns a dictionary containing account data
        """
        r = self.s.get(url=f"{self.url}/rest/v1/accounts")

        return self.hr(r)

    def get_funds(self) -> dict:
        """

        returns a dictionary containing fund data
        """
        r = self.s.get(url=f"{self.url}/rest/v2/customer/accounts/funds")

        self.hr(r)

    def get_max_min(self, instrument: str) -> dict:
        """

        :param instrument:
        :return: dict
        """

        params = {'instrumentCode': {instrument}}

        r = self.s.get(url=f"{self.url}/v1/equity/value-order/min-max",
                       params=params)
        
        self.hr(r)

    def get_summary(self) -> dict:
        """
        """

        payload = []

        r = self.s.post(url=f"{self.url}/rest/trading/v1/accounts/summary",
                       data=json.dumps(payload))
        
        self.hr(r)

    def get_companies(self) -> list:
        """
        """

        r = self.s.get(url=f"{self.url}/rest/companies")
        
        self.hr(r)

    def get_instruments_info(self, instrument: str) -> dict:
        """
        """

        r = self.s.get(url=f"{self.url}/v2/instruments/additional-info/{instrument}")
        
        self.hr(r)

    def get_order_info(self, instrument: str, quantity: float) -> dict:
        """
        """

        params = {'instrumentCode': f"{instrument}",
                  'quantity': quantity,
                  'positionId': 'null'}
        
        r = self.s.get(url=f"{self.url}/rest/v1/tradingAdditionalInfo")
        
        self.hr(r)

    def get_deviations(self, instrument: str,  _useaskprice: str = "false") -> dict:
        """
        """

        if isinstance(instruments, str) == True:
            instruments = [f"{instruments}"]
        else:
            pass
        

        payload = []

        payload.append(dict({"ticker": f"{instrument}", "useAskPrice": f"{_useaskprice}"}))

        r = self.s.put(url=f"{self.url}charting/v4/batch/deviations")
        
        self.hr(r)

    def get_position(self, position_id: str) -> dict:
        """
        """

        r = self.s.get(url=f"{self.url}/rest/reports/positionHistory/{position_id}")
        
        self.hr(r)

    def get_language(self) -> str:
        """
        """

        r = self.s.get(url=f"{self.url}")

        if r.status_code == 200:
            return r.text
        else:
            return None

    def get_all_results(self, page_number: int) -> dict:
        """
        """

        params = {
            "page": page_number,
            "itemsPerPage": 10,
        }

        r = self.s.get(url=f"{self.url}/rest/reports/results",
                       params=params)
        
        self.hr(r)

    def get_order_hist(self, page_number: int, _tz: str = "01:00") -> dict:
        """
        """

        endperiod = (self.now - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00.000+")
        startperiod = self.now.strftime("%Y-%m-%dT23:59:59.173+")

        params = {
            "page": page_number,
            "itemsPerPage": 10,
            "from": f"{endperiod}{_tz}",
            "to": f"{startperiod}{_tz}",
            "filter": "all"
        }

        r = self.s.get(url=f"{self.url}/rest/reports/orders",
                       params=params)
        
        self.hr(r)

    def get_position_hist(self, page_number: int,  _tz: str = "01:00") -> dict:
        """
        """
        endperiod = (self.now - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00.000+")
        startperiod = self.now.strftime("%Y-%m-%dT23:59:59.173+")

        params = {
            "page": page_number,
            "itemsPerPage": 10,
            "from": f"{endperiod}{_tz}",
            "to": f"{startperiod}{_tz}",
            "filter": "all"
        }

        r = self.s.get(url=f"{self.url}/rest/reports/positions",
                       params=params)

        self.hr(r)

    def set_limits(self, position_id: str, TP: float = None, SL: float = None, notify: str = "NONE") -> dict:
        """
        """

        # Get position info
        data = self.get_position(position_id=position_id)

        direction = data[0]["direction"]
        price = data[0]["price"]

        if direction == "buy":
            if TP != None and SL != None:
                tp = round(float(price) + TP, 2)
                sl = round(float(price) - SL, 2)
                payload = {"tp_sl": {"takeProfit": tp, "stopLoss": sl}, 
                           "notify": notify}
            elif TP == None and SL != None:
                sl = round(float(price) - SL, 2)
                payload = {"tp_sl": {"stopLoss": sl}, 
                           "notify": notify}
            elif TP != None and SL == None:
                tp = round(float(price) + TP, 2)
                payload = {"tp_sl": {"takeProfit": tp}, 
                           "notify": notify}
                
        elif direction == "sell":
            if TP != None and SL != None:
                tp = round(float(price) - TP, 2)
                sl = round(float(price) + SL, 2)
                payload = {"tp_sl": {"takeProfit": tp, "stopLoss": sl}, 
                           "notify": notify}
            elif TP == None and SL != None:
                sl = round(float(price) + SL, 2)
                payload = {"tp_sl": {"stopLoss": sl}, 
                           "notify": notify}
            elif TP != None and SL == None:
                tp = round(float(price) - TP, 2)
                payload = {"tp_sl": {"takeProfit": tp}, 
                           "notify": notify}
                
        else:
            return {"code":"failedToGetPosition"}
        
        r = self.s.put(url=f"{self.url}/rest/v2/pending-orders/associated/{position_id}",
                       data=json.dumps(payload))

        self.hr(r)
        
    def add_trailing_stop(self, position_id: str, distance: float, notify: str = "NONE"):
        """
        Add a trailing stop to you live positions.
        :param position_id:
        :param distance:
        :param notify:
        :return:
        """
        data = self.get_position(position_id=position_id)

        direction = data[0]["direction"]
        price = data[0]["price"]

        if direction == "buy":
            distance = distance
        elif direction == "sell":
            distance = distance*-1
        else:
            return 

        payload = {"ts": {"distance": distance}, "notify": f"{notify}"}

        r = self.s.put(url=f"{self.url}/rest/v2/pending-orders/associated/{position_id}",
                       data=json.dumps(payload))
        
        self.hr(r)

    def fundamentals(self, instrument: str, language: str = "en") -> dict:
        """
        """

        params = {
            "languageCode": language,
            "ticker": instrument
        }

        r = self.s.get(url=f"{self.url}/rest/companies/v2/fundamentals",
                       params=params)
        
        self.hr(r)

    def profit_losses(self, instrument: str) -> dict:
        """
        """

        payload = [instrument]

        r = self.s.post(url=f"{self.url}/rest/v2/trading/profit-losses",
                       data=json.dumps(payload))
        
        self.hr(r)

    def high_low(self, instrument: str) -> dict:
        """
        """

        payload = {"ticker": f"{instrument}"}

        r = self.s.post(url=f"{self.url}/charting/v2/batch/high-low",
                       data=json.dumps(payload))
        
        self.hr(r)

    def additional_info(self, instrument: str) -> dict:
        """
        
        """

        params = instrument

        r = self.s.get(url=f"{self.url}/rest/v2/instruments/additional-info/",
                       params=params)
        
        self.hr(r)

    def settings(self, instrument: str) -> dict:
        """
        """
        payload = [instrument]

        r = self.s.post(url=f"{self.url}/rest/v2/account/instruments/settings",
                       data=json.dumps(payload))
        
        self.hr(r)

    def market_order(self,
                     instrument: str,
                     target_price: float,
                     quantity: int,
                     take_profit: float,
                     stop_loss: int,
                     notify: str = "NONE") -> dict:
        
        """
        """
        payload = {'instrumentCode': f"{instrument}",
                   'limitDistance': take_profit,
                   'notify': f"{notify}",
                   'quantity': quantity,
                   'stopDistance': stop_loss,
                   'targetPrice': target_price}
        
        r = self.s.get(url=f"{self.url}/rest/v2/trading/open-positions",
                       data=json.dumps(payload))
        
        return self.hr(r)

    def limit_order(self,
                     instrument: str,
                     target_price: float,
                     quantity: int,
                     take_profit: float,
                     stop_loss: int,
                     notify: str = "NONE") -> dict:

        payload = {'instrumentCode': f"{instrument}",
                   'limitDistance': take_profit,
                   'notify': f"{notify}",
                   'quantity': quantity,
                   'stopDistance': stop_loss,
                   'targetPrice': target_price}
        
        r = self.s.post(url=f"{self.url}/rest/v2/pending-orders/entry-dep-limit-stop/{instrument}",
                       data=json.dumps(payload))

        return self.hr(r)
    
    def close_position(self, position_id: str, current_price: float) -> dict:
        """
        """

        data = self.get_position(position_id=position_id)

        quantity = data[0]["quantity"]

        current_price = self.fast_price()

        payload = {'coeff': {
            'positionId': f'{position_id}',
            'quantity': quantity,
            'targetPrice': current_price}}
        
        r = self.s.delete(url=f"{self.url}/rest/v2/trading/open-positions/close/{position_id}",
                       data=json.dumps(payload))

        return self.hr(r)
    
    def cancel_all_orders(self) -> dict:
        """
        """
        payload = []

        data = r = self.s.post(url=f"{self.url}/rest/trading/v1/accounts/summary",
                       data=json.dumps(payload))
        
        r = self.s.delete(url=f"{self.url}/rest/v2/pending-orders/cancel",
                                headers=self.headers, data=data)
        
        return self.hr(r)
    
    def cancel_order(self, order_id: str) -> dict:
        """
        """
        payload = {'positionId': f'{order_id}'}

        r = self.s.delete(url=f"{self.url}/rest/v2/pending-orders/entry/{order_id}",
                                headers=self.headers, data=json.dumps(payload))

        return self.hr(r)
    
    def _reset(self, account_id: int, amount: int, currency_code: str):
        """"""
        payload = {"accountId": account_id, 
                   "amount": amount, 
                   "currencyCode": f"{currency_code}", 
                   "reason": "settings"}

        r = self.s.post(f"{self.url}/rest/v1/account/reset-with-sum",
                        data=json.dumps(payload))

        return self.hr(r)
        
    def fast_price(self, instrument: str,  _useaskprice: str = "false") -> float:
        """
        """
        payload = {"candles":[{"ticker": f"{instrument}", 
                            "useAskPrice": _useaskprice, 
                            "period": "ONE_MINUTE", "size": 1}]}
        
        r = self.s.put(f"{self.url}/charting/v3/candles",
                        data=json.dumps(payload))
        
        if r.status_code == 200:
            price = r.json()
            return float(price[0]["response"]["candles"][0][-2])
        else:
            return None
        
    def chart_data(self, 
                   instrument: str, 
                   _useaskprice: str = "false", 
                   period: str = "ONE_MINUTE", 
                   size: int = 500) -> list:
        
        """
        """
        payload = {"candles":[{"ticker": f"{instrument}", "useAskPrice": _useaskprice, 
                                 "period": f"{period}", "size": size}]}
        
        r = self.s.put(f'{self.url}/charting/v3/candles', headers=self.headers,
                             data=json.dumps(payload))
        
        if r.status_code == 200:
            return self.hr(r)
        else:
            return None
    
    def multi_price(self, instruments: list, _useaskprice: str = "false") -> dict:
        """
        :param instruments:
        :param _useaskprice:
        :return: [{'ticker': 'TSLA', 'price': 253.49}, 
            {'ticker': 'AAPL', 'price': 182.08}, 
            {'ticker': 'GOOG', 'price': 128.44}]
        """

        payload = {"candles":[]}
        
        for instrument in instruments:
            payload["candles"].append(dict({"ticker": f"{instrument}", "useAskPrice": _useaskprice, 
                                 "period": "ONE_MINUTE", "size": 1}))
            
        r = self.s.put(f'{self.url}/charting/v3/candles', headers=self.headers,
                             data=json.dumps(payload))
        
        if r.status_code == 200:
            result = []
            data = r.json()

            for i in enumerate(data):
                try:
                    result.append(dict({"ticker":data[i[0]]["request"]["ticker"], "price": float(data[i[0]]["response"]["candles"][0][-2])}))
                except IndexError as em:
                    pass
                except KeyError as em:
                    pass
                
            return result
        
        else:
            return None


class Equity(Apit212):

    def __init__(self, mode: str = "demo") -> None:
        super().__init__("EQUITY")
        
        self.url= f"https://{mode}.trading212.com"

        print(self.session)
        r = self.session.get(self.url)
        print(r.headers)
