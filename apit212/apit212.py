# this unofficial API was created by Flock92 originally made to automate my CFD trading on the trading212 platform

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import timedelta
from datetime import datetime
from datetime import timezone
from getpass import getpass
from os import system, name
from .apitconstant import *
from time import sleep
import logging
import json
import sys


class Apit212:
    headers = {}
    now = datetime.now(tz=timezone.utc)

    def __init__(
            self,
            username: str = None,
            password: str = None,
            timeout: int = 2,
            interval: float = 5.0,
            mode: str = 'demo',
            headers: dict = None,
            _beautiful: bool = True):
        """login to t212 account to get credentials to run API

        :param username: trading212 account username
        :type username: str
        :param password: trading212 account password
        :type password: str
        :param timeout: login attempt limits
        :type timeout: int
        :param interval: adjust for slow internet connections
        :type interval: float
        :param mode: set to 'demo' by default
        :type interval: str
        """
        # CLEAR CONSOLE
        if _beautiful == True:
            if name == "nt": # for windows 
                system('cls')
            else: # for mac and linux(here, os.name is 'posix')
                system('clear')

        # START LOGGING
        self._processing_flush(0, index=12) # progressbar
        logging.basicConfig(filename="apit212.log",
                            format='%(asctime)s :: %(levelname)s :: %(message)s',
                            filemode='w')

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.info(f'timeout: {timeout}, interval: {interval}, mode: {mode}')

        self._processing_flush(1, index=12) # progressbar
        # CHECK PARAM'S
        if isinstance(username, str):
            pass
        else:
            username = None

        if isinstance(password, str):
            pass
        else:
            password = None

        if isinstance(timeout, int):
            pass
        else:
            raise TypeError(':param timeout: invalid input')

        if isinstance(interval, (int, float)):
            pass
        else:
            raise TypeError(':param interval: invalid input')

        if isinstance(mode, str) and mode in ['demo', 'live']:
            pass
        else:
            raise TypeError(':param mode: invalid input :: expected "demo" or "live" ')

        # set variables for functions
        self.url = f'https://{mode}.trading212.com/'
        options = webdriver.FirefoxOptions()
        options.add_argument('--log-level=3')
        options.add_argument('-headless')
        my_cookie = None

        self._processing_flush(3, index=12) # progressbar

        # Get login details if no information was passed.
        if username is None:
            username = input('username: ')
            if _beautiful == True:
                if name == "nt": # for windows 
                    system('cls')
                else: # for mac and linux(here, os.name is 'posix')
                    system('clear')
            self._processing_flush(4, index=12)
        elif password is None:
            password = getpass('password: ')
            if _beautiful == True:
                if name == "nt": # for windows 
                    system('cls')
                else: # for mac and linux(here, os.name is 'posix')
                    system('clear')
            self._processing_flush(4, index=12)
        else:
            pass

        # STARTUP WEBDRIVER
        d = webdriver.Firefox(options=options)

        try:
            d.get(url=URL)
            self.logger.info(msg=f'successfully loaded {URL}')
        except Exception as em:
            self.logger.error(em)

        self._processing_flush(4, index=12) # progressbar

        # CHECK URL
        if d.current_url != URL:
            self.logger.error("can not verify URL"), quit(d.close())
        else:
            pass

        d.implicitly_wait(30)

        self._processing_flush(5, index=12) # progressbar

        # START LOGIN PROCESS
        while True:
            if isinstance(headers, dict) or timeout == 0:
                break
            else:
                pass
            timeout -= 1
            try:
                d.find_element(By.XPATH, f"{COOKIE_POPUP}").click()
                self.logger.info('cookie popup closed')
            except Exception as em:
                self.logger.error(f'failed to close cookies popup: {em}')
                continue
            sleep(interval)
            try:
                d.find_element(By.XPATH, f"{LOGIN_BUTTON}").click()
                self.logger.info('login form opened')
            except Exception as em:
                self.logger.error(f'failed to open login form: {em}')
                continue

            self._processing_flush(6, index=12) # progressbar

            # INPUT DETAILS
            try:
                d.find_element(By.NAME, "email").send_keys(username)
                self.logger.info('input username')
            except Exception as em:
                self.logger.error(f'failed to input username: {em}')
                continue
            try:
                d.find_element(By.NAME, "password").send_keys(password)
                self.logger.info('input password')
            except Exception as em:
                self.logger.error(f'failed to input password: {em}')
                continue
            try:
                d.find_element(By.XPATH, f"{SUBMIT_BUTTON}").click()
                self.logger.info('form submitted')
            except Exception as em:
                self.logger.error(f'failed submit form: {em}')
                continue
            sleep(interval)
            try:
                d.execute_script("arguments[0].click();", d.find_element(By.XPATH, f"{POPUP_CLOSE}"))
                self.logger.info('popup closed')
            except Exception as em:
                self.logger.warning(f'failed to close popup: {em}')
                continue
            try:
                user_name = d.find_element(By.XPATH, f"{USER_NAME}").text
                self.logger.info('username verified')
            except Exception as em:
                self.logger.error(f'failed to verify username: {em}')
                continue

            self._processing_flush(7, index=12) # progressbar

            # VERIFY LOGIN
            if username in user_name:
                self.logger.info('successfully logged into account.')
                break
            else:
                self.logger.warning(f'failed logging attempt :: {timeout}')
                pass

        self._processing_flush(8, index=12) # progressbar

        # SWITCH ACCOUNT TYPE
        try:
            d.get(f"https://{mode}.trading212.com")
            self.logger.info(f'switched to "{mode}"')
        except Exception as em:
            self.logger.error(f'failed to switch to {mode}: {em}')

        sleep(interval)

        self._processing_flush(9, index=12) # progressbar

        # GET COOKIES
        user_agent = d.execute_script("return navigator.userAgent;")

        if isinstance(headers, dict):
            self.headers = headers
        else:
            cookies = d.get_cookies()
            for cookie in cookies:
                if cookie['name'] == f'TRADING212_SESSION_{mode.upper()}':
                    my_cookie = f"TRADING212_SESSION_{mode.upper()}={cookie['value']};"
                else:
                    pass

            self.headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": user_agent,
                "Cookie": f'{my_cookie}',
            }

        self.logger.info(f'finished setup...{username}')

        self._processing_flush(11, index=12) # progressbar

        # CLOSE ALL DRIVERS
        d.quit()

        self._processing_flush(12, index=12) # progressbar

        # PRINT CREDENTIALS TO CONFIRM LOGIN
        user_info = self.get_account()[f"{mode}Accounts"][0]

        print("\rSuccessfully connected to userID: ",user_info["id"],
              "type:",user_info["type"],"tradingType",user_info["tradingType"])

    # RETURNS HEADERS AND URL
    def __getitem__(self, key: str):
        """
        :key:
        :return:

        """
        if key == "headers":
            return self.headers
        else:
            return "No value 'key' passed"
    
    def _processing_flush(self, n, index=5):
        if n % index == 0:
            sys.stdout.write(f"\rProcessing [{n}:{index}]%s " % (index * ""))
        sys.stdout.write(f"\rProcessing [{n}:{index}]%s " % ((n % index)* "#"))
        sys.stdout.flush()
    
    # FIND DETAILS OF A INSTRUMENT INCLUDING ISIN
    def find_instrument(self, instrument: str):
        """
        :param instrument:
        :return:

        """
        payload = [instrument]

        try:
            r = requests.post(f"{self.url}/rest/instrumentarium/v2/instruments/find", headers=self.headers,
                              data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message": em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()
    
    # SWITCH ACCOUNT BETWEEN EQUITY AND CFD
    def switch(self):
        """
        :return:

        """
        accountID = self.auth_validate()["accountId"]

        payload = {"accountId": accountID}

        try:
            r = requests.post(f"{self.url}/rest/v1/login/accounts/switch")
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}

        return r.json()
    
    def fast_price(self, instrument: str, _useaskprice: str = "false") -> float:
        """
        :param instrument:
        :return: float

        """
        payload = {"candles":[{"ticker": f"{instrument}", "useAskPrice": _useaskprice, 
                                 "period": "ONE_MINUTE", "size": 1}]}
        try:
            r = requests.put(f'{self.url}/charting/v3/candles', headers=self.headers,
                             data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        price = r.json()
        result = float(price[0]["response"]["candles"][0][-2])

        return result
        
    # GET CHART DATA
    def chart_data(self, instrument: str, _useaskprice: str = "false", 
                   period: str = "ONE_MINUTE", size: int = 500) -> list:
        """
        :param instruments:
        :param period: ONE_MINUTE, FIVE_MINUTES, TEN_MINUTES, ONE_MONTH
        :param _useaskprice:
        :param size:
        :return: [{'request': {'ticker': 'TSLA', 'period': 'ONE_MINUTE', 'size': 500, 
            'useAskPrice': False}, 'response': {'candles': [[1691152740000, 259.6, 259.97, 
            259.43, 259.49, 47], [1691152800000, 259.38, 259.94, 259.17, 259.56, 58], 
            [1691152860000, 259.62, 260.34, 259.62, 260.19, 42]

        """
        payload = {"candles":[{"ticker": f"{instrument}", "useAskPrice": _useaskprice, 
                                 "period": f"{period}", "size": size}]}
        
        try:
            r = requests.put(f'{self.url}/charting/v3/candles', headers=self.headers,
                             data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()
    
    # GET THE CURRENT PRICE
    def live_price(self, instruments: list, 
                   _useaskprice: str = "false") -> dict:
        """
        :param instruments:
        :param _useaskprice:
        :return: [{'ticker': 'TSLA', 'price': 253.49}, 
            {'ticker': 'AAPL', 'price': 182.08}, 
            {'ticker': 'GOOG', 'price': 128.44}]

        """
        if isinstance(instruments, str) == True:
            instruments = [f"{instruments}"]
        else:
            pass
        
        payload = {"candles":[]}

        for instrument in instruments:
            payload["candles"].append(dict({"ticker": f"{instrument}", "useAskPrice": _useaskprice, 
                                 "period": "ONE_MINUTE", "size": 1}))
       
        try:
            r = requests.put(f'{self.url}/charting/v3/candles', headers=self.headers,
                             data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        result = []
        data = r.json()
        
        for i in enumerate(data):
            result.append(dict({"ticker":data[i[0]]["request"]["ticker"], "price": float(data[i[0]]["response"]["candles"][0][-2])}))
                         
        return result

    # GET AUTH VALIDATE
    def auth_validate(self) -> dict:
        """
        :return: {'id': '********-****-****-****-************', 'accountId': ********, 'customerId': ********,
        'tradingType': 'CFD', 'customerUuid': '********-****-****-****-************', 'frontend': 'WC4',
        'readyToTrade': True, 'deviceUuid': ''}
        """

        try:
            r = requests.get(f'{self.url}/auth/validate', headers=self.headers)
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()

    # GET ACCOUNT DETAILS
    def get_account(self) -> dict:
        """Get account info

        :return: {'demoAccounts': [{'id': ********, 'type': 'DEMO', 'tradingType': 'CFD',
        'customerId': ********, 'createdDate': '2023-01-17T03:20:48.000+00:00',
        'status': 'ACTIVE', 'registerSource': 'WC4', 'currencyCode': 'GBP', 'readyToTrade': True}],
        'liveAccounts': [{'id': ********, 'type': 'LIVE', 'tradingType': 'CFD', 'customerId': ********,
        'createdDate': '2023-01-17T03:20:32.000+00:00', 'status': 'PENDING_ACTIVATION', 'registerSource': 'WC4',
        'currencyCode': 'GBP', 'readyToTrade': False}]}
        """

        try:
            r = requests.get(f'{self.url}/rest/v1/accounts', headers=self.headers)
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()

    # GET ACCOUNT FUNDS
    def get_funds(self) -> dict:
        """Get account funds

        :return: dict={'*********': {'accountId': ********,
        'tradingType': 'CFD', 'currency': 'GBP', 'freeForWithdraw': 310.5,
        'freeForCfdTransfer': 0, 'total': 4954.12, 'lockedCash': {'totalLockedCash': 0, 'lockedCash': []}}}
        """

        try:
            r = requests.get(f"{self.url}/rest/v2/customer/accounts/funds", headers=self.headers)
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()

    # GET ORDER SIZE
    def get_max_min(self, instrument: str) -> dict:
        """
        Get the min and max 'BUY' & 'SELL' for an instrument passed to this function.

        :param instrument:
        :return: {'minBuy': 1.0, 'maxBuy': 4593.17,
        'minSell': 1.0, 'maxSell': 0.0, 'sellThreshold': 0.0, 'maxSellQuantity': 0}

        """
        params = {'instrumentCode': {instrument}}

        try:
            r = requests.get(f"{self.url}/v1/equity/value-order/min-max",
                             headers=self.headers, params=params)
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()

    # CANCEL ORDER
    def cancel_order(self, order_id: str) -> dict:
        """

        :param order_id:
        :return: {'account': {'dealer': 'AVUSUK', 'positions': [{'positionId': '********-****-****-****-************',
        'humanId': '**********', 'created': '2023-06-05T21:32:45.000+03:00', 'modified': None, 'averagePrice': 181.09,
        'averagePriceConverted': 144.96174516, 'currentPrice': 186.45, 'limitPrice': None, 'stopPrice': None,
        'value': 16047.62, 'investment': 15945.79, 'limitStopNotify': None, 'trailingStop': None,
        'trailingStopPrice': None, 'trailingStopNotify': None, 'code': 'AAPL', 'margin': 3225.65, 'ppl': 461.33,
        'quantity': 110.0, 'maxBuy': None, 'maxSell': None, 'maxOpenBuy': None, 'maxOpenSell': None, 'swap': -16.11,
        'frontend': 'WC4', 'pplAdjustment': None, 'autoInvestQuantity': None, 'fxPpl': None}
        """
        payload = {'positionId': f'{order_id}'}

        try:
            r = requests.delete(url=f"{self.url}/rest/v2/pending-orders/entry/{order_id}",
                                headers=self.headers, data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()
    
    # CANCEL ALL PENDING ORDERS
    def cancel_all_orders(self) -> dict:
        """"""
        payload = []

        try:
            data = requests.post(url=f"{self.url}/rest/trading/v1/accounts/summary",
                                 headers=self.headers, data=json.dumps(payload))
        except ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        try:
            r = requests.delete(url=f"{self.url}/rest/v2/pending-orders/cancel",
                                headers=self.headers, data=data)
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}

        return r.json()

    # CANCEL ORDER
    def close_position(self, position_id: str, quantity: float, current_price: float) -> dict:
        """
        close open positions
        :param position_id:
        :param quantity:
        :param current_price:
        :return:
        """

        payload = {'coeff': {
            'positionId': f'{position_id}',
            'quantity': quantity,
            'targetPrice': current_price}}

        try:
            r = requests.delete(url=f"{self.url}/rest/v2/trading/open-positions/close/{position_id}",
                                headers=self.headers, data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()

    # GET ACCOUNT SUMMARY (GET POSITION ID)
    def get_summary(self) -> dict:
        """This function can be used along with a bot to get positionId's to manually close positions and get data on
        your accounts.

        :return: {'cash': {'free': 219.73, 'total': 4851.04, 'interest': -379.02, 'indicator': 51, 'commission': 0.0,
        'cash': 5000.0, 'ppl': 327.56, 'result': -97.5, 'margin': 4631.31, 'spreadBack': 0.0, 'nonRefundable': 0.0,
        'dividend': 0.0, 'totalCashForWithdraw': 219.73}, 'open': {'unfilteredCount': 3,
        'items': [{'positionId': '********-****-****-****-************', 'humanId': '**********',
        'created': '2023-06-05T21:32:45.000+03:00', 'averagePrice': 181.09,
        'averagePriceConverted': 144.96174516, 'currentPrice': 186.31, 'value': 16013.4,
        'investment': 15945.79, 'code': 'AAPL', 'margin': 3218.77, 'ppl': 448.66,
        'quantity': 110.0, 'swap': -16.08, 'frontend': 'WC4'}
        """
        payload = []

        try:
            r = requests.post(url=f"{self.url}/rest/trading/v1/accounts/summary", headers=self.headers,
                              data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}

        return r.json()

    # GET LIST OF COMPANIES
    def get_companies(self) -> list:
        """
        This function will return a list of tickers and their corresponding isin code.
        :return: [{'ticker': 'TICK', 'isin': '*************'}]
        """
        try:
            r = requests.get(f"{self.url}/rest/companies", headers=self.headers)
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}

        return r.json()

    # GET TICKER INFORMATION
    def get_instruments_info(self, instrument: str) -> dict:
        """
        This function returns information about the ticker.
        :param instrument:
        :return: {'code': 'TSLA', 'type': 'STOCK', 'margin': 0.2,
        'shortPositionSwap': -0.06510720836211, 'longPositionSwap': -0.25863029163789,
        'tsSwapCharges': '1970-01-01T23:00:00.000+02:00', 'marginPercent': '20', 'leverage': '1:5'}
        """
        try:
            r = requests.get(f'{self.url}/v2/instruments/additional-info/{instrument}',
                             headers=self.headers)
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}

        return r.json()

    # GET INSTRUMENT INFORMATION
    def get_order_info(self, instrument: str, quantity: float):
        """
        This function will return the buy and sell margins info and swap info
        :param instrument:
        :param quantity:
        :return: {'buyMargin': 39.74, 'sellMargin': 39.74, 'buySwap': -0.2, 'sellSwap': -0.05}
        """
        params = {'instrumentCode': f"{instrument}",
                  'quantity': quantity,
                  'positionId': 'null'}
        try:
            r = requests.get(f"{self.url}/rest/v1/tradingAdditionalInfo", 
                             headers=self.headers, params=params)
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()

    # GET ASK PRICE FOR INSTRUMENT
    def get_deviations(self, instruments: list, _useaskprice: str = "false") -> list:
        """

        :param instrument:
        :param _useaskprice:
        :return: [{'request': {'ticker': '****', 'useAskPrice': False}, 'response':
        {'timestamp': 1687852810000, 'price': 250.37, 'period': 'd1'}}]
        """

        if isinstance(instruments, str) == True:
            instruments = [f"{instruments}"]
        else:
            pass
        

        payload = []

        for instrument in instruments:
            payload.append(dict({"ticker": f"{instrument}", "useAskPrice": f"{_useaskprice}"}))

        try:
            r = requests.put(f'{self.url}charting/v1/watchlist/batch/deviations',
                             headers=self.headers, data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}

        return r.json()

    # PLACE LIMIT ORDER
    def limit_order(self,
                    instrument: str,
                    quantity: float,
                    target_price: float,
                    take_profit: float,
                    stop_loss: float,
                    notify: str = "NONE"):
        """the minimum requirement to submit a limit order is the instrument, quantity and target price.
        You can also set a take_profit and stop_loss limits. I would like to point out that this
        function will only submit your order and will make no attempts to change any of the parameters.

        :param instrument:
        :param quantity:
        :param target_price:
        :param take_profit:
        :param stop_loss:
        :param notify:
        :return:
        """
        payload = {'quantity': round(quantity, 1),
                   'targetPrice': round(target_price, 2),
                   'takeProfit': round(take_profit, 2),
                   'stopLoss': round(stop_loss, 2),
                   'notify': notify}
        
        try:
            r = requests.post(f'{self.url}/rest/v2/pending-orders/entry-dep-limit-stop/{instrument}',
                              headers=self.headers, data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}

        return r.json()

    # MARKET ORDER
    def market_order(self,
                     instrument: str,
                     target_price: float,
                     quantity: int,
                     limit_distance: float,
                     stop_distance: int,
                     notify: str = "NONE"):
        """the minimum requirement to submit a market order is the instrument, quantity and target price.
        You can also set a take_profit and stop_loss limits. I would like to point out that this
        function will only submit your order and will make no attempts to change any of the parameters.

        if an incorrect order is submitted you will get a code message returned.
        ie: {'code': 'BusinessException', 'context': {'max': 684, 'type': 'InsufficientFundsMaxBuy'},
        'message': 'InsufficientResourcesException'}

        :param instrument:
        :param target_price:
        :param limit_distance:
        :param notify:
        :param quantity:
        :param stop_distance:
        :return:
        """

        payload = {'instrumentCode': f"{instrument}",
                   'limitDistance': limit_distance,
                   'notify': f"{notify}",
                   'quantity': quantity,
                   'stopDistance': stop_distance,
                   'targetPrice': target_price}

        try:
            r = requests.post(url=f"{self.url}/rest/v2/trading/open-positions",
                              headers=self.headers, data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}

        return r.json()

    # ADD TRAILING STOP LOSS
    def trailing_stop(self, position_id: str, distance: float, notify: str = "NONE"):
        """
        Add a trailing stop to you live positions.
        :param position_id:
        :param distance:
        :param notify:
        :return:
        """

        payload = {"ts": {"distance": distance}, "notify": f"{notify}"}

        try:
            r = requests.put(f"{self.url}/rest/v2/pending-orders/associated/{position_id}",
                             headers=self.headers, data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}

        return r.json()
    
    # ADD A STOP LOSS OR TAKE PROFIT TO OPEN TRADES
    def add_limits(self, position_id: str, TP: float = None, SL: float = None, notify: str = "NONE"):
        """
        Add or change a stoploss and takeprofit on an open order.
        :param position_id:
        :param TP:
        :param SL:
        :param notify:
        :return: 
        """
        # GET POSTION DIRECTION AND PRICE
        data = self.get_position(position_id=position_id)

        direction = data[0]["direction"]
        price = data[0]["price"]

        payload = {"tp_sl": {}, "notify": notify}

        if direction == "buy":
            if TP != None:
                payload["tp_sl"].update(dict({"takeProfit": round(float(price) + TP, 2)}))
            else:
                pass

            if SL != None:
                payload["tp_sl"].update(dict({"stopLoss": round(float(price) - SL, 2)}))
            else:
                pass
        elif direction == "sell":
            if TP != None:
                payload["tp_sl"].update(dict({"takeProfit": round(float(price) - TP, 2)}))
            else:
                pass

            if SL != None:
                payload["tp_sl"].update(dict({"stopLoss": round(float(price) + SL, 2)}))
            else:
                pass
        else:
            return {"Excaption": {"message": "failed to update tp_sl"}}
        
        try:
            r = requests.put(f"{self.url}/rest/v2/pending-orders/associated/{position_id}", 
                             headers=self.headers, data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()
    
    # GET POSITION HISTORY
    def all_position_hist(self, _tz: str = "01:00") -> dict:
        """
        :return: 
        """

        endperiod = (self.now - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00.000+")
        startperiod = self.now.strftime("%Y-%m-%dT23:59:59.173+")
        result = []

        params = {
            "page": 1,
            "itemsPerPage": 10,
            "from": f"{endperiod}{_tz}",
            "to": f"{startperiod}{_tz}",
            "filter": "all"
        }

        try:
            r = requests.get(f"{self.url}/rest/reports/positions",
                            headers=self.headers, params=params)
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        limit = 0
        while True:
            if r.status_code == 403:
                break
            data = r.json()
            result.append(data)
            try:
                nextpage = r.json()["nextPage"]
                limit += 1
                params = {
                    "page": limit,
                    "itemsPerPage": 10,
                    "from": f"{endperiod}{_tz}",
                    "to": f"{startperiod}{_tz}",
                    "filter": "all"
                }
            except KeyError as em:
                break
            try:
                r = requests.get(f"{self.url}/rest/reports/positions",
                            headers=self.headers, params=params)
            except requests.exceptions.ConnectionError as em:
                return {"code":"connectionError", "message":em}
            except requests.exceptions.Timeout as em:
                return {"code": "requestTimeout", "message": em}
            except requests.exceptions.HTTPError as em:
                return {"code": "HTTPError", "message": em}
            except requests.exceptions.RequestException as em:
                return {"code": "Unknown", "message": em}
        
        return result

    # GET ORDERS
    def all_order_hist(self, _tz: str = "01:00") -> dict:
        """
        """
        
        endperiod = (self.now - timedelta(days=1)).strftime("%Y-%m-%dT00:00:00.000+")
        startperiod = self.now.strftime("%Y-%m-%dT23:59:59.173+")
        result = []

        params = {
            "page": 1,
            "itemsPerPage": 10,
            "from": f"{endperiod}{_tz}",
            "to": f"{startperiod}{_tz}",
            "filter": "all"
        }
        
        try:
            r = requests.get(f"{self.url}/rest/reports/orders",
                            headers=self.headers, params=params)
        except ConnectionError as em:
            return {"code":"connectionError", "message":em}
        
        limit = 0
        while True:
            if r.status_code == 403:
                break
            data = r.json()
            result.append(data)
            try:
                nextpage = r.json()["nextPage"]
                limit += 1
                params = {
                    "page": limit,
                    "itemsPerPage": 10,
                    "from": f"{endperiod}{_tz}",
                    "to": f"{startperiod}{_tz}",
                    "filter": "all"
                }
            except KeyError as em:
                break
            r = requests.get(f"{self.url}/rest/reports/orders",
                        headers=self.headers, params=params)
        
        return result

    # GET OPEN POSISTIONS            
    def get_position(self, position_id: str):
        """
        :params position_id:
        :return: [{'eventType': {'action': 'opened', 'source': 'MARKET_ORDER'}, 
                'eventNumber': {'name': 'MO30****9640', 'id': '274****13', 'frontend': 'WC4'}, 'time': '2023-08-02T22:42:54.000+03:00', 
                'direction': 'sell', 'quantity': 1.0, 'price': '105.29', 'avgQuantity': 1.0, 'avgPrice': '105.2900', 'modifiedDirection': 
                'sell'}]
        """
        try:
            r = requests.get(f"{self.url}/rest/reports/positionHistory/{position_id}", 
                             headers=self.headers)
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}

        return r.json()

    # VALIDATE SESSION
    def validate_session(self):
        """
        :return: {'id': '*****-********-********-******', 'accountId': **********, 
                'customerId': *********, 'tradingType': 'CFD', 
                'customerUuid': '*****-********-********-******', 'frontend': 'WC4', 
                'readyToTrade': True, 'deviceUuid': ''}

        """
        try:
            r = requests.get(f"{self.url}validate-session", headers=self.headers)
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}

        return r.status_code

    # RESET DEMO ACCOUNT
    def _reset(self, account_id: int, amount: int, currency_code: str):
        """"""
        payload = {"accountId": account_id, "amount": amount, "currencyCode": f"{currency_code}", "reason": "settings"}

        r = requests.post(f"{self.url}/rest/v1/account/reset-with-sum", headers=self.headers, data=json.dumps(payload))

        return r
    
    def settings(self, instrument: str):
        """
        :param instrument:
        :return: [{'code': 'TSLA', 'maxBuy': 4.7, 'maxMarketOrderBuy': 1.8, 'maxSell': 4.7, 
                'maxOpenBuy': 1200.0, 'maxOpenSell': 1200.0, 'suspended': False, 'minTrade': 0.1}]

        """

        payload = [instrument]

        try:
            r = requests.post(f"{self.url}/rest/v2/account/instruments/settings", headers=self.headers,
                              data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
    
        return r.json()
    
    def additional_info(self, instrument: str):
        """

        :param instrument:
        :return: {code: "STLD_US_CFD", type: "STOCK", margin: 0.2, shortPositionSwap: -0.026087881955975,…}

        """

        params = instrument

        try:
            r = requests.get(f"{self.url}/rest/v2/instruments/additional-info/", 
                             headers=self.headers, params=params)
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()
    
    def high_low(self, instrument: str):
        """
        :param instrument:
        :return: {request: {ticker: "EURUSD"}, result: {high: 1.10339, low: 1.10002}}
        
        """

        payload = {"ticker": f"{instrument}"}

        try:
            r = requests.post(f"{self.url}/charting/v2/batch/high-low",
                              headers=self.headers, data=json.dumps(payload))
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()

    def profit_losses(self, instrument: str):
        """
        :param instrument:
        :return: {'data': [{'profit': 1.28223115578, 'loss': 1.267194029851}], 
                'size': 1, 'positiveSum': 0, 'negativeSum': 0}
        """

        payload = [instrument]

        try:
            r = requests.post(f"{self.url}/rest/v2/trading/profit-losses", headers=self.headers,
                              data=json.dumps(payload))   
        except requests.exceptions.ConnectionError as em:
            return {"code":"connectionError", "message":em}
        except requests.exceptions.Timeout as em:
            return {"code": "requestTimeout", "message": em}
        except requests.exceptions.HTTPError as em:
            return {"code": "HTTPError", "message": em}
        except requests.exceptions.RequestException as em:
            return {"code": "Unknown", "message": em}
        
        return r.json()
    
