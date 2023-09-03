# this unofficial API was created by Flock92 originally made to automate my CFD trading on the trading212 platform
# https://www.youtube.com/watch?v=_YVQN6_nkfs

from selenium.webdriver.common.by import By
from requests import Session
from selenium import webdriver
from requests import Response
from requests_html import HTML
from datetime import timedelta
from bs4 import BeautifulSoup
from threading import Thread
from apitconstant import *
from typing import Any
from time import sleep
import pandas as pd
import pickle
import logging
import datetime
import requests
import time
import json
import js2py
import sys
import os

# THINGS TO ADD TO THE SETUP

"""
https://live.trading212.com/rest/sunshine/v1/tokens get

https://www.trading212.com/api/geolocation # returns global location

https://62a7491e21ae5c00f273a9de.config.smooch.io/sdk/v2/integrations/62a7491e21ae5c00f273a9de/config GET RETURNS ID 629ee56e85859000f10378a7
https://api.smooch.io/sdk/v2/apps/629ee56e85859000f10378a7/appusers/4ad24efd169b7779e936a7a7 GET 


GET
	https://www.trading212.com/_next/static/chunks/pages/cfd-ec974f600be3155c.js javascript
"""


class _Constant:

    running = False
    error = False
    error_msg = ""
    func_name = ""

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
            for s in symbols:
                sys.stdout.write(f"\rProcessing {self.func_name} %s " % (f"{s}"))
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


class Apit212:

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
               }
    
    cookies = ""
    
    session = Session()

    constant = _Constant()

    username = ""

    mode = "demo"

    def __init__(self, str = None, timeout: int = 2, interval: float = 0.5, Longinterval: float = 10) -> None:

        # handle files
        self.fh = FileHandler()

        # set variables
        self.timeout = timeout
        self.interval = interval
        self.Longinterval = Longinterval

        # setup logging file
        logging.basicConfig(filename="apit212.log",
                            format='%(asctime)s :: %(levelname)s :: %(message)s',
                            filemode='w')

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.info(f'timeout: {timeout}, interval: {interval}')

        self.user = self.username

    def _reconnect(self) -> None:
        """
        """
        cookies = self.fh.read_file(filename="_cookies")

        self.session.headers = self.headers

        for cookie in cookies:
            # Set trading212_session
            if cookie['name'] == f'TRADING212_SESSION_{self.mode.upper()}':
                self.session.cookies.set(f"TRADING212_SESSION_{self.mode.upper()}", cookie["value"])
            
            # Set customer_session
            if cookie['name'] == "CUSTOMER_SESSION":
                self.session.cookies.set("CUSTOMER_SESSION", cookie["value"])
   
        r = self.session.get(url=f"https://{self.mode}.trading212.com/")
        
        #print(r)
        #print(requests.get(url="https://.trading212.com/auth/validate", headers=self.headers))

        r = self.session.get(url=f"https://{self.mode}.trading212.com/auth/validate")

        print(r)

        if r.status_code == 200:
            self.constant.end()
            return r.status_code
        else:
            self.fh.delete_file(filename="_cookies")
            self.build_driver()

    def _get_token_experimental(self) -> dict:
        """
        """
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

        r = self.session.post(url=f"{self.url}/api/authentication/authenticate")

        token = soup.find("input", id="recaptcha-token")["value"]

        #token = str(input).split('"')
        #print(soup.find("input", id="recaptcha-token")) # GET VALUE FOR LOGIN REQUEST

        # Login 
        #loginUrl = "https://www.trading212.com/api/authentication/login"

        #r = requests.post(url=loginUrl, headers=self.headers,
        #                 data=json.dumps(payload), timeout=(3, 22))
        #
        return token
             
    def setup(self, username: str, password: str, _beauty: bool = True, mode: str = "demo") -> None:
        """
        :param username:
        :param password:
        """
        self.mode = mode

        # clear console
        if _beauty == True:
            if os.name == "nt": # for windows 
                os.system('cls')
            else: # for mac and linux(here, os.name is 'posix')
                os.system('clear')

        self.constant._start_flush("Setup")

        # if cookies file exisit and session files exist try login
        if self.fh.check_file(filename="_cookies") == True:

            self.username = username # required to re-establish connection

            self._reconnect()

        else:

            self.build_driver()

    def build_driver(self) -> None:
        """
        """

        # Get the correct url
        self.url = f'https://{self.mode}.trading212.com/'
        # Setup webdriver
        options = webdriver.FirefoxOptions()
        options.add_argument('--log-level=3')
        options.add_argument('-headless')

        # start webdriver & get main page
        d = webdriver.Firefox(options=options)
        d.implicitly_wait(60)
        d.get(url=URL)
        if d.current_url == URL:
            self.logger.info(f"Successfully loaded: {URL}")
        else:
            self.logger.error(f"Failed to load: {URL}")
            errmsg = "Failed to load page."
            self.constant.end_error(error_msg=errmsg)
        while self.timeout > 0:
            try:
                d.find_element(By.XPATH, f"{COOKIE_POPUP}").click()
                self.logger.info('cookie popup closed')
            except Exception as em:
                self.logger.error(f'failed to close cookies popup: {em}') 
            else:
                pass
            sleep(self.interval)
            try:
                d.find_element(By.XPATH, f"{LOGIN_BUTTON}").click()
                self.logger.info('login form opened')
            except Exception as em:
                self.logger.error(f'failed to open login form: {em}')
            else:
                pass
            
            try:
                d.find_element(By.NAME, "email").send_keys(username)
                self.logger.info('input username')
            except Exception as em:
                self.logger.error(f'failed to input username: {em}')
            else:
                pass
                
            try:
                d.find_element(By.NAME, "password").send_keys(password)
                self.logger.info('input password')
            except Exception as em:
                self.logger.error(f'failed to input password: {em}')
            else:
                pass
                
            try:
                d.find_element(By.XPATH, f"{SUBMIT_BUTTON}").click()
                self.logger.info('form submitted')
            except Exception as em:
                self.logger.error(f'failed submit form: {em}')
            else:
                pass
            #sleep(self.Longinterval)
            while True:
                try:
                    d.find_element(By.XPATH, '/html/body/div[1]/div[5]/div[1]')
                    break
                except Exception as em:
                    self.logger.info('waiting for page to load')
            attempt = 5
            while attempt != 0:
                d.implicitly_wait(5)
                # VERIFY LOGIN
                try:
                    user_name = d.find_element(By.XPATH, f"{USER_NAME[1]}").text
                    self.logger.info('username verified')
                except Exception as em:
                    self.logger.info(em)
                try:
                    user_name = d.find_element(By.XPATH, f"{USER_NAME[0]}").text
                    self.logger.info('username verified')
                except Exception as em:
                    self.logger.info(em)
                try:
                    if str(username) == str(user_name):
                        self.logger.info('successfully logged into account.')
                        break
                except Exception as em:
                    self.logger.error(f'failed to verify username: {em}')
                    attempt -= 1
            if 'user_name' in locals():
                break
            self.timeout -= 1
        
        # Switch account type
        while True:
            d.get(f"https://{self.mode}.trading212.com")
            current_url = d.current_url
            if current_url == self.url:
                break
            else:
                sleep(self.interval)

        sleep(self.Longinterval)
        # save cookies
        cookies = d.get_cookies()
        
        for cookie in cookies:
            if f"TRADING212_SESSION_{self.mode.upper()}" in cookie['name']:
                self.session.cookies.set(cookie['name'], cookie['value'])
            
            if "CUSTOMER_SESSION" in cookie["name"]:
                self.session.cookies.set(cookie['name'], cookie['value'])

            if "LOGIN_TOKEN" in cookie["name"]:
                self.session.cookies.set(cookie['name'], cookie['value'])

        self.cookies = cookies
        self._cleanup_driver(driver=d)
        self.fh.create_file(filename="_cookies", data=self.cookies)
        self.constant.end()
        self.session.headers = self.headers

    def _cleanup_driver(self, driver, _end: bool = False) -> None:
        """
        """
        driver.close()

        driver.quit()

        del driver

        if _end == True:
            quit()


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
            return data
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


class CFD(Apit212):

    now = datetime.datetime.now()

    def __init__(self, dealer: str = "AVUSUK", lang: str = "EN") -> None:

        self.fh = FileHandler()

        super().__init__()

        self.url= f"https://{self.mode}.trading212.com"

        # Get sessions from main class
        self.s = self.session

        # Check connection
        validate = self.auth_validate()

        if "code" in validate:
            if validate["code"] == "AuthenticationFailed":
                quit("Failed to validate session")
        
        # Get account username
        self.user = self.user

        # Get account info
        accountInfo = self.get_account()[f"{self.mode}Accounts"]

        for info in accountInfo:
            if info["tradingType"] == "CFD":
                accountId = info["id"]
            else:
                pass

        # Confirm correct account
        authAccount = self.auth_validate()["accountId"]

        if str(authAccount) != str(accountId):
            # switch accound    
            self.switch(account_id=accountId)
        else:
            pass

    def switch(self, account_id: str) -> dict:
        """
        """

        payload = {"accountId": account_id}

        r = self.s.post(url=f"{self.url}/rest/v1/login/accounts/switch",
                        data=json.dumps(payload))

        return r.json()

    def update_headers(self, headers: dict) -> None:
        """
        update sessions headers

        :param headers:
        """
        self.s.headers = headers

        self.fh.update_file("_cookies", headers)

    def auth_validate(self) -> dict:
        """
        get information about session
        """
        r = self.s.get(url=f"{self.url}/auth/validate")

        if r.status_code == 401:
            return r.json()
        else:
            return r.json()
 
    def authenticate(self) -> dict:
        """
        re-establish session if session has ended and update headers
        """

        r = self.s.get(url=f"{self.url}/rest/v1/webclient/authenticate")

        return r.json()


    def get_timezone(self) -> dict:
        """
        """

        r = self.s.get(url=f"{self.url}/rest/v2/time-zones")

        return r.json()
    
    def get_account(self) -> dict:
        """
        returns a dictionary containing account data
        """
        r = self.s.get(url=f"{self.url}/rest/v1/accounts")

        return r.json()

    def get_funds(self) -> dict:
        """

        returns a dictionary containing fund data
        """
        r = self.s.get(url=f"{self.url}/rest/v2/customer/accounts/funds")

        return r.json()

    def get_max_min(self, instrument: str) -> dict:
        """

        :param instrument:
        :return: dict
        """

        params = {'instrumentCode': {instrument}}

        r = self.s.get(url=f"{self.url}/v1/equity/value-order/min-max",
                       params=params)
        
        return r.json()

    def get_summary(self) -> dict:
        """
        """

        payload = []

        r = self.s.post(url=f"{self.url}/rest/trading/v1/accounts/summary",
                       data=json.dumps(payload))
        
        return r.json()

    def get_companies(self) -> list:
        """
        """

        r = self.s.get(url=f"{self.url}/rest/companies")
        
        return r.json()

    def get_instruments_info(self, instrument: str) -> dict:
        """
        """

        r = self.s.get(url=f"{self.url}/v2/instruments/additional-info/{instrument}")
        
        return r.json()

    def get_order_info(self, instrument: str, quantity: float) -> dict:
        """
        """

        params = {'instrumentCode': f"{instrument}",
                  'quantity': quantity,
                  'positionId': 'null'}
        
        r = self.s.get(url=f"{self.url}/rest/v1/tradingAdditionalInfo")
        
        return r.json()

    def get_deviations(self, instruments: list and str,  _useaskprice: str = "false") -> dict:
        """
        """
        if isinstance(instruments, str):
            instruments = [instruments]

        payload = []

        for instrument in instruments:
            payload.append(dict({"ticker": f"{instrument}", "useAskPrice": f"{_useaskprice}"}))

        r = self.s.put(url=f"{self.url}/charting/v1/watchlist/batch/deviations",
                       data=json.dumps(payload))
        
        return r.json()

    def get_position(self, position_id: str) -> dict:
        """
        """

        r = self.s.get(url=f"{self.url}/rest/reports/positionHistory/{position_id}")
        
        return r.json()

    def get_all_results(self, page_number: int) -> dict:
        """
        """

        params = {
            "page": page_number,
            "itemsPerPage": 10,
        }

        r = self.s.get(url=f"{self.url}/rest/reports/results",
                       params=params)
        
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

        r = self.s.get(url=f"{self.url}/rest/reports/orders",
                       params=params)
        
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

        r = self.s.get(url=f"{self.url}/rest/reports/positions",
                       params=params)

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
        
        r = self.s.put(url=f"{self.url}/rest/v2/pending-orders/associated/{position_id}",
                       data=json.dumps(payload))

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

        r = self.s.put(url=f"{self.url}/rest/v2/pending-orders/associated/{position_id}",
                       data=json.dumps(payload))
        
        return r.json()

    def fundamentals(self, instrument: str, language: str = "en") -> dict:
        """
        """

        params = {
            "languageCode": language,
            "ticker": instrument
        }

        r = self.s.get(url=f"{self.url}/rest/companies/v2/fundamentals",
                       params=params)
        
        return r.json()

    def profit_losses(self, instrument: str) -> dict:
        """
        """

        payload = [instrument]

        r = self.s.post(url=f"{self.url}/rest/v2/trading/profit-losses",
                       data=json.dumps(payload))
        
        return r.json()

    def high_low(self, instrument: str) -> dict:
        """
        """

        payload = {"ticker": f"{instrument}"}

        r = self.s.post(url=f"{self.url}/charting/v2/batch/high-low",
                       data=json.dumps(payload))
        
        return r.json()

    def additional_info(self, instrument: str) -> dict:
        """
        
        """
        r = self.s.get(url=f"{self.url}/rest/v2/instruments/additional-info/{instrument}")
        
        return r.json()

    def settings(self, instrument: str) -> dict:
        """
        """
        payload = [instrument]

        r = self.s.post(url=f"{self.url}/rest/v2/account/instruments/settings",
                       data=json.dumps(payload))
        
        return r.json()

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
        
        return r.json()

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
        
        r = self.s.delete(url=f"{self.url}/rest/v2/trading/open-positions/close/{position_id}",
                       data=json.dumps(payload))

        return r.json()
    
    def cancel_all_orders(self) -> dict:
        """
        """
        payload = []

        data = r = self.s.post(url=f"{self.url}/rest/trading/v1/accounts/summary",
                       data=json.dumps(payload))
        
        r = self.s.delete(url=f"{self.url}/rest/v2/pending-orders/cancel",
                                headers=self.headers, data=data)
        
        return r.json()
    
    def cancel_order(self, order_id: str) -> dict:
        """
        """
        payload = {'positionId': f'{order_id}'}

        r = self.s.delete(url=f"{self.url}/rest/v2/pending-orders/entry/{order_id}",
                                headers=self.headers, data=json.dumps(payload))

        return r.json()
    
    def _reset(self, account_id: int, amount: int, currency_code: str):
        """"""
        payload = {"accountId": account_id, 
                   "amount": amount, 
                   "currencyCode": f"{currency_code}", 
                   "reason": "settings"}

        r = self.s.post(f"{self.url}/rest/v1/account/reset-with-sum",
                        data=json.dumps(payload))

        return r.json()
        
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
            return r.json()
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

    def __init__(self, dealer: str = "AVUSUK", lang: str = "EN") -> None:

        self.fh = FileHandler()

        super().__init__()

        self.url= f"https://{self.mode}.trading212.com"

        # Get sessions from main class
        self.s = self.session

        # Check connection
        self.auth_validate()
        
        # Get account username
        self.user = self.user

        # Get account info
        accountInfo = self.get_account()[f"{self.mode}Accounts"]

        for info in accountInfo:
            if info["tradingType"] == "EQUITY":
                accountId = info["id"]
                print(accountId)
            else:
                pass

        # Confirm correct account
        authAccount = self.auth_validate()["accountId"]

        if str(authAccount) != str(accountId):
            # switch accound    
            print(self.switch(account_id=accountId))

        else:
            pass

    def switch(self, account_id: str) -> dict:
        """
        """

        payload = {"accountId": account_id}

        r = self.s.post(url=f"{self.url}/rest/v1/login/accounts/switch",
                        data=json.dumps(payload))

        return r.json()
    
    def get_account(self) -> dict:
        """
        returns a dictionary containing account data
        """
        r = self.s.get(url=f"{self.url}/rest/v1/accounts")

        return r.json()

    def auth_validate(self) -> dict:
        """
        get information about session
        """
        r = self.s.get(url=f"{self.url}/auth/validate")

        if r.status_code == 401:
            return r.json()
        else:
            return r.json()
 
    def authenticate(self) -> dict:
        """
        re-establish session if session has ended and update headers
        """

        r = self.s.get(url=f"{self.url}/rest/v1/webclient/authenticate")

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
        
        r = self.s.put(f'{self.url}/charting/v3/candles/close', headers=self.headers,
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
                        data=json.dumps(payload))
        
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
        
        r = self.s.post(url=f"{self.url}/rest/public/v2/equity/order",
                        data=json.dumps(payload))
        
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
        
        r = self.s.post(url=f"{self.url}/rest/public/v2/equity/order",
                        data=json.dumps(payload))
        
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

        r = self.s.post(url=f"{self.url}/rest/public/v2/equity/order",
                        data=json.dumps(payload))
        
        return r.json()
    
    def cancel_order(self,
                     position_id: str) -> dict:
        """
        """

        r = self.s.get(url=f"{self.url}/rest/public/v2/equity/order/{position_id}")
        
        return r.json()
    
    def min_max(self, instrument: str, currency: str) -> dict:
        """
        """

        params = {"instrumentCode": instrument, "currencyCode": currency}

        r = self.s.get(url=f"{self.url}/rest/v1/equity/value-order/min-max",
                       params=params)
        
        return r.json()
    
