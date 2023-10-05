# This script was created by flock92 to simplify using the trading212 api

import requests
import json
from .Constant import *
from time import sleep
from datetime import timedelta
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
import logging
import sys
import os
from typing import Any
import pandas as pd

from selenium.common.exceptions import ScreenshotException

class _Constant:

    running = False
    error = False
    error_msg = ""
    func_name = ""
    txt = ""

    def __init__(self) -> None:
        pass

    def _start_flush(self, func_name: str) -> None:
        try:
            if self.thread.is_alive() == True:
                self.end()
        except AttributeError:
            pass
        self.func_name = func_name
        self.running = True
        self.thread = Thread(target=self._processing_flush)
        self.thread.daemon = True
        self.thread.start()

    def _processing_flush(self) -> None:
        """
        """
        self.running = True

        symbols = ["$=","+#","%^","|:",">£",";D"]
        
        sys.stdout.write(f"Processing {self.func_name} %s " % ("£"))

        while self.running == True:
            sys.stdout.write('\x1b[2K')
            for s in symbols:
                sys.stdout.write(f"\rProcessing {self.func_name} {self.txt} %s " % (f"{s}"))
                sleep(0.2)

        if self.error == True:
            sys.stdout.write('\x1b[2K')
            sys.stdout.write(f"\rFailed {self.func_name} {self.error_msg} %s \n" % (":(   "))
            sys.stdout.flush()        
        else:
            sys.stdout.write('\x1b[2K')
            sys.stdout.write(f"\rFinished {self.func_name} %s \n" % (":)   "))
            sys.stdout.flush()

    def end(self):

        self.running = False

        try:
            while True:
                if self.thread.is_alive() == True:
                    sleep(0.1)
                else:
                    break
        except UnboundLocalError as em:
            pass
        except AttributeError as em:
            pass

        try:
            del self.thread
        except UnboundLocalError as em:
            pass
        except AttributeError as em:
            pass

    def end_error(self, error_msg: str):

        self.error_msg = error_msg

        self.running = False

        try:
            while True:
                if self.thread.is_alive() == True:
                    sleep(0.5)
                else:
                    break
        except UnboundLocalError as em:
            pass
        except AttributeError as em:
            pass

        try:
            del self.thread
        except UnboundLocalError as em:
            pass
        except AttributeError as em:
            pass

    def _update_txt(self, func_name: str) -> None:
        """
        """
        self.txt = func_name


class _FileHandler:

    directory = ""

    def __init__(self) -> None:
        pass
    
    def create_file(self, filename: str, data: dict) -> None:
        """
        Creates a new file.

        :param filename:
        :param data:
        """
        path = f"{self.directory}{filename}.csv"

        pd.to_pickle(data, path)

    def delete_file(self, filename: str) -> None:
        """
        Delete existing file:
        
        :param filename:
        """
        path = f"{self.directory}{filename}.csv"

        if os.path.isfile(path) == True:
            os.remove(path)

    def read_file(self, filename: str) -> dict:
        """
        Read and exisitng pickled file.

        :param filename:
        :Returns dict:
        """
        path = f"{self.directory}{filename}.csv"

        if os.path.isfile(path) == True:
            data = pd.read_pickle(path)
            return data
        else:
            return {"code":"fileNotFound"}

    def update_file(self, filename: str, data: dict) -> None:
        """
        Adds a dictionary to an existing file

        :param filename:
        :param data:
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
        :param filename:
        Returns a bool 
        """
        path = f"{self.directory}{filename}.csv"

        return os.path.isfile(path=path) 
    
    def overwrite_file(self, filename: str, data: dict) -> None:
        """
        Overwrite exisitng files

        :param filename:
        :param data:
        """
        path = f"{self.directory}{filename}.csv"

        if os.path.isfile(path=path) == True:
            file = self.read_file(filename=filename)
            file = data
            pd.to_pickle(file, path)
        else:
            self.create_file(filename=filename, data=data)


class Apit212:

    interval = 0.5
    implicit = 30
    delay = 10
    directory = None
    _saveCookies = False

    def __init__(self) -> None:

        self.headers = HEADERS
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

        self.fh = _FileHandler()
        self.constant = _Constant()

    def setup(self, username: str, password: str, mode: str, timeout: int = 2, _beauty: bool = True) -> None:
        """
        """
        # clear console
        if _beauty == True:
            if os.name == "nt": # for windows 
                os.system('cls')
            else: # for mac and linux(here, os.name is 'posix')
                os.system('clear')

        self.mode = mode

        self.constant._start_flush(func_name="Setup")

        # Get the correct url
        self.url = f'https://{mode}.trading212.com'

        # Add to headers
        self.headers.update(dict({
            "Host":f"{mode}.trading212.com",
            "Origin":f"https://{mode}.trading212.com",
            "Referer":f"https://{mode}.trading212.com/",
        }))

        # Check existing headers
        if self.fh.check_file(filename="_cookies") == True:

            # Check saved headers 
            self._reconnect()

        # If connection failed reconnects
        if self.fh.check_file(filename="_cookies") == False: 

            # Setup webdriver
            options = webdriver.FirefoxOptions()
            options.add_argument('--log-level=3')
            options.add_argument('-headless')

            # start webdriver & get main page
            self.constant._update_txt(func_name="Selenium")

            d = webdriver.Firefox(options=options)

            d.get(url=URL)

            d.implicitly_wait(self.implicit)

            if d.current_url == URL:
                self.logger.info(f"Successfully loaded: {URL}")
            else:
                self.logger.error(f"Failed to load: {URL}")
                errmsg = "Failed to load page."
                self.constant.end_error(error_msg=errmsg)
                return 0

            while timeout > 0:

                sleep(self.delay) # wait for main page to load

                try:
                    d.find_element(By.XPATH, f"{COOKIE_POPUP}").click()
                    self.logger.info('cookie popup closed')
                except Exception as em:
                    self.logger.error(f'Initial popup: {em}') 
                else:
                    pass

                sleep(self.interval)

                try:
                    d.find_element(By.XPATH, f"{LOGIN_BUTTON}").click()
                    self.logger.info('login form opened')
                except Exception as em:
                    self.logger.error(f'Login Form: {em}')
                else:
                    pass
                
                try:
                    d.find_element(By.NAME, "email").send_keys(username)
                    self.logger.info('Username input: sentKeys')
                except Exception as em:
                    self.logger.error(f'Username input: {em}')
                else:
                    pass

                try:
                    d.find_element(By.NAME, "password").send_keys(password)
                    self.logger.info('Password input: sentKeys')
                except Exception as em:
                    self.logger.error(f'Password input: {em}')
                else:
                    pass

                try:
                    d.find_element(By.XPATH, f"{SUBMIT_BUTTON}").click()
                    self.logger.info('Submit form successful.')
                except Exception as em:
                    self.logger.error(f'Submit form: {em}')
                else:
                    pass

                sleep(self.delay) # Wait for main page to load
                
                break

            d.get(f"https://{mode}.trading212.com") # Switch account type

            sleep(self.delay)
            
            self.constant._update_txt(func_name="cookies")

            cookies = d.get_cookies() # Get cookies

            if self._saveCookies == True:
                self.fh.create_file(filename="_cookies", data=cookies)

            self.headers['Cookie'] = ""

            # Update header variable
            for cookie in cookies:
                if f"TRADING212_SESSION_{self.mode.upper()}" in cookie['name']:
                    self.headers["Cookie"] += f"{cookie['name']}={cookie['value']};"
                if "CUSTOMER_SESSION" in cookie["name"]:
                    self.headers["Cookie"] += f"{cookie['name']}={cookie['value']};"
                if "LOGIN_TOKEN" in cookie["name"]:
                    self.headers["Cookie"] += f"{cookie['name']}={cookie['value']};"
                if "_rdt_uuid" in cookie["name"]:
                    self.headers["Cookie"] += f"{cookie['name']}={cookie['value']};"

            sleep(self.interval)
    
            r = requests.get(url=f"{self.url}/auth/validate", headers=self.headers)

            if r.status_code == 200:
                self.constant.end()
                return r.status_code
            else:
                self.constant.end()
                return r.status_code    

    def _reconnect(self) -> None:
        """
        """

        self.constant._start_flush(func_name="_Reconnect")
        
        # Get cookie file
        cookies = self.fh.read_file(filename="_cookies")

        # Update header variable
        for cookie in cookies:
            if f"TRADING212_SESSION_{self.mode.upper()}" in cookie['name']:
                self.headers["Cookie"] += f"{cookie['name']}={cookie['value']};"
            if "CUSTOMER_SESSION" in cookie["name"]:
                self.headers["Cookie"] += f"{cookie['name']}={cookie['value']};"
            if "LOGIN_TOKEN" in cookie["name"]:
                self.headers["Cookie"] += f"{cookie['name']}={cookie['value']};"
            if "_rdt_uuid" in cookie["name"]:
                self.headers["Cookie"] += f"{cookie['name']}={cookie['value']};"
   
        r = requests.get(url=f"{self.url}", headers=self.headers)
        
        r = requests.get(url=f"{self.url}/auth/validate", headers=self.headers)

        if r.status_code == 200:
            self.constant.end()
            return r.status_code
        else:
            self.fh.delete_file(filename="_cookies")
            self.headers['Cookie'] = ""
            return r.status_code


class CFD(object):

    def __init__(self, cred: Apit212, dealer: str = "AVUSUK", lang: str = "EN") -> None:

        # Create time object
        self.now = datetime.now()

        # Get Mode
        self.mode = cred.mode

        # Get the correct url
        self.url = f'https://{cred.mode}.trading212.com'

        # headers
        self.headers = cred.headers

        # Get account info
        account = self.get_account()[f"{cred.mode}Accounts"]

        for info in account:
            if info["tradingType"] == "CFD":
                accountId = info["id"]
            else:
                pass

        # Confirm correct account
        authAccount = self.auth_validate()["accountId"]

        if str(authAccount) != str(accountId):
            # switch accound    
            self.__switch(account_id=accountId)

        else:
            pass

    def __switch(self, account_id: int) -> dict:
        """
        """

        payload = {"accountId":int(account_id)}

        data = self.auth_validate()

        self.headers.__setitem__("X-Trader-Client" , f"application=WC4, version=2.4.48, accountId={account_id}, dUUID={data['customerUuid']}")

        r = requests.post(url=f"{self.url}/rest/v1/login/accounts/switch",
                          headers=self.headers, data=json.dumps(payload))
        
        # update cookies in headers
        cookies = r.cookies

        # update cookies in headers
        cookies = r.cookies

        for cookie in cookies:
            self.headers["Cookie"] = ""
            self.headers["Cookie"] += f"{cookie.name}={cookie.value};"


        return r.json()

    def auth_validate(self) -> dict:
        """
        get information about session
        """
        r = requests.get(url=f"{self.url}/auth/validate", headers=self.headers)

        return r.json()
 
    def authenticate(self) -> dict:
        """
        re-establish session if session has ended and update headers
        """

        r = requests.get(url=f"{self.url}/rest/v1/webclient/authenticate", headers=self.headers)

        return r.json()

    def get_timezone(self) -> dict:
        """
        Returns all timezones
        """

        r = requests.get(url=f"{self.url}/rest/v2/time-zones", headers=self.headers)

        return r.json()
    
    def get_account(self) -> dict:
        """
        returns a dictionary containing account data
        """
        r = requests.get(url=f"{self.url}/rest/v1/accounts", headers=self.headers)

        return r.json()

    def get_funds(self) -> dict:
        """
        returns a dictionary containing fund data
        """
        r = requests.get(url=f"{self.url}/rest/v2/customer/accounts/funds", headers=self.headers)

        return r.json()

    def get_max_min(self, instrument: str) -> dict:
        """
        :param instrument:
        :return: dict
        """

        params = {'instrumentCode': {instrument}}

        r = requests.get(url=f"{self.url}/v1/equity/value-order/min-max", 
                         headers=self.headers, params=params)
        
        return r.json()

    def get_summary(self) -> dict:
        """
        """

        payload = []

        r = requests.post(url=f"{self.url}/rest/trading/v1/accounts/summary",
                          headers=self.headers, data=json.dumps(payload))
        
        return r.json()

    def get_companies(self) -> list:
        """
        Returns all companies avalible on the trading212 platform
        """

        r = requests.get(url=f"{self.url}/rest/companies", headers=self.headers)
        
        return r.json()

    def get_instruments_info(self, instrument: str) -> dict:
        """
        Get information about a specific instrument
        :param instrument:
        :return dict:
        """

        r = requests.get(url=f"{self.url}/v2/instruments/additional-info/{instrument}", 
                         headers=self.headers)
        
        return r.json()

    def get_order_info(self, instrument: str, quantity: float) -> dict:
        """
        Returns order history as a dictionary:
        :param insturment:
        :param quantity:
        :return dict:
        """

        params = {'instrumentCode': f"{instrument}",
                  'quantity': quantity,
                  'positionId': 'null'}
        
        r = requests.get(url=f"{self.url}/rest/v1/tradingAdditionalInfo", 
                         headers=self.headers, params=params)
        
        return r.json()

    def get_deviations(self, instruments: list and str,  _useaskprice: str = "false") -> dict:
        """
        """
        if isinstance(instruments, str):
            instruments = [instruments]

        payload = []

        for instrument in instruments:
            payload.append(dict({"ticker": f"{instrument}", "useAskPrice": f"{_useaskprice}"}))

        r = requests.put(url=f"{self.url}/charting/v1/watchlist/batch/deviations",
                         headers=self.headers, data=json.dumps(payload))
        
        return r.json()

    def get_position(self, position_id: str) -> dict:
        """
        """

        r = requests.get(url=f"{self.url}/rest/reports/positionHistory/{position_id}",
                         headers=self.headers,)
        
        return r.json()

    def get_all_results(self, page_number: int) -> dict:
        """
        """

        params = {
            "page": page_number,
            "itemsPerPage": 10,
        }

        r = requests.get(url=f"{self.url}/rest/reports/results",
                         headers=self.headers, params=params)
        
        return r.json()

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

        r = requests.get(url=f"{self.url}/rest/reports/orders", 
                         headers=self.headers, params=params)
        
        return r.json()

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

        r = requests.get(url=f"{self.url}/rest/reports/positions",
                         headers=self.headers, params=params)

        return r.json()

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
        
        r = requests.put(url=f"{self.url}/rest/v2/pending-orders/associated/{position_id}",
                         headers=self.headers, data=json.dumps(payload))

        return r.json()
        
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
            return {"code":"noDirection"}

        payload = {"ts": {"distance": distance}, "notify": f"{notify}"}

        r = requests.put(url=f"{self.url}/rest/v2/pending-orders/associated/{position_id}", 
                         headers=self.headers, data=json.dumps(payload))
        
        return r.json()

    def fundamentals(self, instrument: str, language: str = "en") -> dict:
        """
        """

        params = {
            "languageCode": language,
            "ticker": instrument
        }

        r = requests.get(url=f"{self.url}/rest/companies/v2/fundamentals",
                         headers=self.headers, params=params)
        
        return r.json()

    def profit_losses(self, instrument: str) -> dict:
        """
        """

        payload = [instrument]

        r = requests.post(url=f"{self.url}/rest/v2/trading/profit-losses", 
                          headers=self.headers, data=json.dumps(payload))
        
        return r.json()

    def high_low(self, instrument: str) -> dict:
        """
        """

        payload = {"ticker": f"{instrument}"}

        r = requests.post(url=f"{self.url}/charting/v2/batch/high-low", 
                          headers=self.headers, data=json.dumps(payload))
        
        return r.json()

    def additional_info(self, instrument: str) -> dict:
        """
        
        """
        r = requests.get(url=f"{self.url}/rest/v2/instruments/additional-info/{instrument}",
                         headers=self.headers,)
        
        return r.json()

    def settings(self, instrument: str) -> dict:
        """
        """
        payload = [instrument]

        r = requests.post(url=f"{self.url}/rest/v2/account/instruments/settings", 
                          headers=self.headers, data=json.dumps(payload))
        
        return r.json()

    def market_order(self,
                     instrument: str,
                     target_price: float,
                     quantity: float,
                     take_profit: float,
                     stop_loss: float,
                     notify: str = "NONE") -> dict:
        
        """
        """
        payload = {'instrumentCode': f"{instrument}",
                   'limitDistance': take_profit,
                   'notify': f"{notify}",
                   'quantity': quantity,
                   'stopDistance': stop_loss,
                   'targetPrice': target_price}
        
        r = requests.post(url=f"{self.url}/rest/v2/trading/open-positions", 
                         headers=self.headers, data=json.dumps(payload))
        
        return r.json()

    def limit_order(self,
                     instrument: str,
                     target_price: float,
                     quantity: float,
                     take_profit: float,
                     stop_loss: float,
                     notify: str = "NONE") -> dict:

        payload = {'instrumentCode': f"{instrument}",
                   'limitDistance': take_profit,
                   'notify': f"{notify}",
                   'quantity': quantity,
                   'stopDistance': stop_loss,
                   'targetPrice': target_price}
        
        r = requests.post(url=f"{self.url}/rest/v2/pending-orders/entry-dep-limit-stop/{instrument}", 
                          headers=self.headers, data=json.dumps(payload))

        return r.json()
    
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
        
        r = requests.delete(url=f"{self.url}/rest/v2/trading/open-positions/close/{position_id}", 
                            headers=self.headers, data=json.dumps(payload))

        return r.json()
    
    def cancel_all_orders(self) -> dict:
        """
        """
        payload = []

        data = r = requests.post(url=f"{self.url}/rest/trading/v1/accounts/summary",
                       data=json.dumps(payload))
        
        r = requests.delete(url=f"{self.url}/rest/v2/pending-orders/cancel",
                            headers=self.headers, data=data)
        
        return r.json()
    
    def cancel_order(self, order_id: str) -> dict:
        """
        """
        payload = {'positionId': f'{order_id}'}

        r = requests.delete(url=f"{self.url}/rest/v2/pending-orders/entry/{order_id}",
                            headers=self.headers, data=json.dumps(payload))

        return r.json()
    
    def _reset(self, account_id: int, amount: int, currency_code: str):
        """
        reset a demo account
        """
        payload = {"accountId": account_id, 
                   "amount": amount, 
                   "currencyCode": f"{currency_code}", 
                   "reason": "settings"}

        r = requests.post(f"{self.url}/rest/v1/account/reset-with-sum",
                        headers=self.headers, data=json.dumps(payload))

        return r.json()
        
    def fast_price(self, instrument: str,  _useaskprice: str = "false") -> float:
        """
        """
        payload = {"candles":[{"ticker": f"{instrument}", 
                            "useAskPrice": _useaskprice, 
                            "period": "ONE_MINUTE", "size": 1}]}
        
        r = requests.put(f"{self.url}/charting/v3/candles", 
                         headers=self.headers, data=json.dumps(payload))
        
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
        
        r = requests.put(f'{self.url}/charting/v3/candles', headers=self.headers,
                             data=json.dumps(payload))
        
        if r.status_code == 200:
            return r.json()
        else:
            return None
    
    def multi_price(self, instruments: list, _useaskprice: str = "false") -> list:
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
            
        r = requests.put(f'{self.url}/charting/v3/candles', headers=self.headers,
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


class Equity(object):

    def __init__(self, cred: Apit212, dealer: str = "AVUSUK", lang: str = "EN") -> None:

        # Create time object
        self.now = datetime.now()

        # Get Mode
        self.mode = cred.mode

        # Get the correct url
        self.url = f'https://{cred.mode}.trading212.com'

        # headers
        self.headers = cred.headers

        # Get account info
        account = self.get_account()[f"{cred.mode}Accounts"]

        for info in account:
            if info["tradingType"] == "EQUITY":
                accountId = info["id"]
            else:
                pass

        # Confirm correct account
        authAccount = self.auth_validate()["accountId"]

        if str(authAccount) != str(accountId):
            # switch accound    
            self.__switch(account_id=accountId)

        else:
            pass

    def __switch(self, account_id: int) -> dict:
        """
        """
        payload = {"accountId":int(account_id)}

        data = self.auth_validate()

        self.headers.__setitem__("X-Trader-Client" , f"application=WC4, version=2.4.48, accountId={account_id}, dUUID={data['customerUuid']}")

        r = requests.post(url=f"{self.url}/rest/v1/login/accounts/switch",
                          headers=self.headers, data=json.dumps(payload))
        
        # update cookies in headers
        cookies = r.cookies

        for cookie in cookies:
            self.headers["Cookie"] = ""
            self.headers["Cookie"] += f"{cookie.name}={cookie.value};"

        return r.json()
    
    def get_account(self) -> dict:
        """
        returns a dictionary containing account data
        """
        r = requests.get(url=f"{self.url}/rest/v1/accounts", headers=self.headers)

        return r.json()

    def auth_validate(self) -> dict:
        """
        get information about session
        """
        r = requests.get(url=f"{self.url}/auth/validate", headers=self.headers)

        return r.json()
 
    def authenticate(self) -> dict:
        """
        re-establish session if session has ended and update headers
        """

        r = requests.get(url=f"{self.url}/rest/v1/webclient/authenticate",  headers=self.headers)

        return r.json()

    def close(self, 
                   instrument: str, 
                   _useaskprice: str = "true", 
                   period: str = "THIRTY_MINUTES", 
                   size: int = 336) -> list:
        
        """
        """
        payload = {"candles":[{"ticker": f"{instrument}", "useAskPrice": _useaskprice, 
                                 "period": f"{period}", "size": size}]}
        
        r = requests.put(f'{self.url}/charting/v3/candles/close', headers=self.headers,
                             data=json.dumps(payload))
        
        if r.status_code == 200:
            return r.json()
        else:
            return None

    def add_cost(self, 
                 instrument: str, 
                 currency: str, 
                 limitPrice: float,
                 orderType: str,
                 quantity: float,
                 stopPrice: float,
                 timeValidity: str = "GOOD_TILL_CANCEL") -> dict:
        """
        """

        payload = {"instrumentCode":instrument,"currencyCode":currency,
                   "limitPrice":limitPrice,"orderType":orderType,"quantity":quantity,
                   "stopPrice":stopPrice,"timeValidity":timeValidity}
        
        r = self.s.post(url=f"{self.url}/rest/public/added-costs", 
                        headers=self.headers, data=json.dumps(payload))
        
        return r.json()
    
    def market_order(self, 
                    instrument: str, 
                    currency: str,
                    quantity: float,
                    timeValidity: str = "GOOD_TILL_CANCEL") -> dict:
        
        """
        """

        payload = {"instrumentCode":instrument,"currencyCode":currency,
                   "orderType":"MARKET","quantity":quantity,
                   "timeValidity":timeValidity}
        
        r = requests.post(url=f"{self.url}/rest/public/v2/equity/order",  
                          headers=self.headers, data=json.dumps(payload))
        
        return r.json()
    
    def limit_order(self, 
                    instrument: str, 
                    currency: str,
                    quantity: float,
                    limit_price: float,
                    timeValidity: str = "GOOD_TILL_CANCEL") -> dict:
        """
        """

        payload = {"instrumentCode":instrument,"currencyCode":
                   currency,"limitPrice":limit_price,"orderType":"LIMIT",
                   "quantity":quantity, "timeValidity":timeValidity}
        
        r = requests.post(url=f"{self.url}/rest/public/v2/equity/order",  
                          headers=self.headers, data=json.dumps(payload))
        
        return r.json()
  
    def stop_limit(self, 
                    instrument: str, 
                    currency: str,
                    quantity: float,
                    limit_price: float,
                    stop_price: float,
                    timeValidity: str = "GOOD_TILL_CANCEL") -> dict:
        """
        """

        payload = {"instrumentCode":instrument,"currencyCode":currency,
                   "limitPrice":limit_price,"orderType":"STOP_LIMIT",
                   "quantity":quantity,"stopPrice":stop_price,"timeValidity":timeValidity}

        r = requests.post(url=f"{self.url}/rest/public/v2/equity/order",  
                        headers=self.headers, data=json.dumps(payload))
        
        return r.json()
    
    def cancel_order(self,
                     position_id: str) -> dict:
        """
        """

        r = requests.get(url=f"{self.url}/rest/public/v2/equity/order/{position_id}",  headers=self.headers)
        
        return r.json()
    
    def min_max(self, instrument: str, currency: str) -> dict:
        """
        """

        params = {"instrumentCode": instrument, "currencyCode": currency}

        r = requests.get(url=f"{self.url}/rest/v1/equity/value-order/min-max",  
                         headers=self.headers, params=params)
        
        return r.json()


class Apitkey:

    def __init__(self) -> None:
        pass

    class Equity:

        def __init__(self, api_key: str, mode: str) -> None:
            """
            Login using the trading212 official API key

            :param API_key:
            :param mode:
            """

            self.mode = mode

            self.delay = 1.5

            self.url = f"https://{mode}.trading212.com/api/v0/equity"
            self.url2 = f"https://{mode}.trading212.com/api/v0"

            self.headers = {"Authorization": f"{api_key}"}

            response = requests.get(url=f"{self.url}/metadata/exchanges", headers=self.headers)

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def exchange_list(self) -> dict:
            """
            """

            sleep(self.delay)

            response = requests.get(url=f"{self.url}/metadata/exchanges", 
                                    headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def instrument_list(self) -> dict:
            """        
            """

            sleep(self.delay)

            response = requests.get(url=f"{self.url}/metadata/instruments", 
                                    headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                pass

        def pies(self) -> dict:
            """
            """
            sleep(self.delay)

            response = requests.get(url=f"{self.url}/pies", 
                                    headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def create_pie(self, 
                       instrument_shares: dict, 
                       end_date: str, goal: int, 
                       dividend_action: str, 
                       icon: str,
                       name: str) -> dict:
            """

            :param instrument_shares:
            :param end_date:
            :param dividend_action:
            :param icon:
            :param name:

            :return: dict     
            """
            sleep(self.delay)

            headers = self.headers

            headers.__setitem__("Content-Type", "application/json")

            payload = {
                "dividendCashAction": dividend_action,
                "endDate": end_date,
                "goal": goal,
                "icon": icon,
                "instrumentShares": instrument_shares,
                "name": name,
            }

            response = requests.post(url=f"{self.url}/pies", 
                                    headers=headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def delete_pie(self, pie_id: str) -> dict:
            """

            :param pie_id:

            :return: dict 
            """
            sleep(self.delay)

            param = pie_id

            response = requests.delete(url=f"{self.url}/pies", 
                                    headers=self.headers, params=param)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def fetch_pie(self, pie_id) -> dict:
            """

            :param pie_id:
            
            :return: dict
            """
            sleep(self.delay)

            headers = self.headers

            headers.__setitem__("Content-Type", "application/json")

            param = pie_id

            response = requests.get(url=f"{self.url}/pies", 
                                    headers=headers, params=param)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def update_pie(self, pie_id: str, 
                       instrument_shares: dict, 
                       end_date: str, goal: int, 
                       dividend_action: str, 
                       icon: str, 
                       name: str) -> dict:
            """

            :param instrument_shares:
            :param end_date:
            :dividend_action:
            :param icon:
            :param name:

            :return dict:
            """
            sleep(self.delay)

            param = pie_id

            payload = {
                "dividendCashAction": dividend_action,
                "endDate": end_date,
                "goal": goal,
                "icon": icon,
                "instrumentShares": instrument_shares,
                "name": name,
            }

            response = requests.get(url=f"{self.url}/pies", 
                                    headers=self.headers, params=param,
                                    json=payload)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def equity_orders(self) -> dict:
            """
            """

            sleep(self.delay)

            response = requests.get(url=f"{self.url}/orders", 
                                    headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def limit_order(self, 
                        limit_price: float, 
                        quantity: float, 
                        instrument: str,
                        time_validity: str) -> dict:
            """

            :param limit_price:
            :param quantity:
            :param instrument:
            :param time_validity:

            :return: dict
            """

            sleep(self.delay)

            headers = self.headers

            headers.__setitem__("Content-Type", "application/json")

            payload = {
                "limitPrice":limit_price,
                "quantity":quantity,
                "ticker":instrument,
                "timeValidity":time_validity
            }

            response = requests.post(url=f"{self.url}/orders/limit", 
                                    headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def market_order(self, instrument: str, quantity: float) -> dict:
            """

            :param instrument:
            :param quantity:

            :return: dict
            """

            sleep(self.delay)

            headers = self.headers

            headers.__setitem__("Content-Type", "application/json")

            payload = {
                "quantity":quantity,
                "ticker":instrument,
            }

            response = requests.post(url=f"{self.url}/orders/market", 
                                    headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def stop_order(self, 
                       instrument: str, 
                       quantity: float, 
                       stop_price: float, 
                       time_validity: str) -> dict:
            """

            :param instrument:
            :param quantity:
            :param stop_price:
            :param time_validity:

            :return: dict
            """

            sleep(self.delay)

            headers = self.headers

            headers.__setitem__("Content-Type", "application/json")

            payload = {
                "quantity":quantity,
                "stopPrice":stop_price,
                "ticker":instrument,
                "timeValidity":time_validity
            }

            response = requests.post(url=f"{self.url}/orders/stop", 
                                    headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def stop_limit_order(self,
                             limit_price: float, 
                             quantity: float, 
                             instrument: str,
                             stop_price: float,
                             time_validity: str, 
                             ) -> dict:
            """

            :param limit_price:
            :param quantity:
            :param instrument:
            :param stop_priceL
            :param time_validity:

            :return: dict        
            """

            sleep(self.delay)

            headers = self.headers

            headers.__setitem__("Content-Type", "application/json")

            payload = {
                "limitPrice":limit_price,
                "quantity":quantity,
                "stopPrice":stop_price,
                "ticker":instrument,
                "timeValidity":time_validity
            }

            response = requests.post(url=f"{self.url}/orders/stop_limit", 
                                    headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def cancel_order(self, order_id) -> dict:
            """

            :param order_id:
            :return: dict
            """

            sleep(self.delay)

            param = order_id

            response = requests.delete(url=f"{self.url}/orders", 
                                    headers=self.headers, params=param)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()
        
        def fetch_order(self, order_id) -> dict:
            """
            :param order_id:
            :return: dict
            """

            sleep(self.delay)

            param = order_id

            response = requests.get(url=f"{self.url}/orders", 
                                    headers=self.headers, params=param)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def account_data(self) -> dict:
            """

            return account cash 
            """

            sleep(self.delay)

            response = requests.get(url=f"{self.url}/account/cash", 
                                    headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def account_meta(self) -> dict:
            """
            returns account meta.
            """

            sleep(self.delay)

            response = requests.get(url=f"{self.url}/account/info", 
                                    headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                return response.status_code
                pass

        def fetch_all_positions(self) -> dict:
            """
            return all positions in dict
            """

            sleep(self.delay)

            response = requests.get(url=f"{self.url}portfolio", 
                                    headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                pass

        def fetch_position(self, instrument: str) -> dict:
            """
            
            :param instrument:
            :return: dict
            """

            sleep(self.delay)

            response = requests.get(url=f"{self.url}/portfolio/{instrument}", 
                                    headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def order_history(self, instrument: str, limit: int = 20, cursor: int = 0) -> dict:
            """

            :param instrument:
            :param limit:
            :param cursor:

            :return: dict
            """

            sleep(self.delay)

            params = {
                "cursor": cursor,
                "ticker": instrument,
                "limit": limit
            }

            response = requests.get(url=f"{self.url}/history/orders", 
                                    headers=self.headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def paid_out_dividends(self, instrument: str, limit: int = 20, cursor: int = 0) -> dict:
            """
            :param instrument:
            :param limit:
            :param cursor:

            :return: dict
            """

            sleep(self.delay)
            
            params = {
                "cursor": cursor,
                "ticker": instrument,
                "limit": limit
            }

            response = requests.get(url=f"{self.url2}/history/dividends", 
                                    headers=self.headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            else:
                pass
            
        def export_list(self) -> list:
            """
            """

            sleep(self.delay)

            response = requests.get(url=f"{self.url2}/history/exports", 
                                    headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def export_csv(self, 
                       time_from: str,
                       time_to: str,
                       include_dividends: bool = True, 
                       include_interest: bool = True,
                       include_orders: bool = True,
                       include_transactions: bool = True):
            """
            :param time_from:
            :param time_to:
            :param include_dividends:
            :param include_interest:
            :param include_orders:
            :param include_transactions:

            :return: csv
            """

            sleep(self.delay)

            headers = self.headers

            headers.__setitem__("Content-Type", "application/json")

            payload = {
                "dataIncluded": {
                    "includeDividends":include_dividends,
                    "includeInterest":include_interest,
                    "includeOrders":include_orders,
                    "includeTransactions":include_transactions,
                },
                "timeFrom": time_from,
                "timeTo": time_to
            }

            response = requests.post(url=f"{self.url2}/history/exports", 
                                    headers=self.headers, json=payload)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()

        def transactions(self, cursor: int = 0, limit: int = 20) -> dict:
            """

            :param cursor:
            :param limit:
            :return: dict
            """

            sleep(self.delay)

            params = {
                "cursor": cursor,
                "limit": limit
            }

            response = requests.get(url=f"{self.url2}/history/transactions", 
                                    headers=self.headers, params=params)
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return response.status_code
            else:
                return response.json()
            
