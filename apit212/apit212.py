# this unofficial API was created by Flock92 originally made to automate my CFD trading on the trading212 platform

# this unofficial API was created by Flock92 originally made to automate my CFD trading on the trading212 platform

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from getpass import getpass
from .apitconstant import *
from time import sleep
import logging
import json


class Apit212:
    headers = {}

    def __init__(
            self,
            username: str,
            password: str,
            timeout: int = 2,
            interval: float = 5.0,
            mode: str = 'demo',
            headers: dict = None):
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

        # START LOGGING
        logging.basicConfig(filename="apit212.log",
                            format='%(asctime)s :: %(levelname)s :: %(message)s',
                            filemode='w')

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.info(f'timeout: {timeout}, interval: {interval}, mode: {mode}')

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
        options.headless = True
        my_cookie = None

        # Get login details if no information was passed.
        if username is None:
            username = input('username: ')
        elif password is None:
            password = getpass('password: ')
        else:
            pass

        # STARTUP WEBDRIVER
        d = webdriver.Firefox(options=options)

        try:
            d.get(url=URL)
            self.logger.info(msg=f'successfully loaded {URL}')
        except Exception as em:
            self.logger.error(em)

        # CHECK URL
        if d.current_url != URL:
            self.logger.error("can not verify URL"), quit(d.close())
        else:
            pass

        d.implicitly_wait(30)

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

            # VERIFY LOGIN
            if username in user_name:
                self.logger.info('successfully logged into account.')
                break
            else:
                self.logger.warning(f'failed logging attempt :: {timeout}')
                pass

        # SWITCH ACCOUNT
        try:
            d.get(f"https://{mode}.trading212.com")
            self.logger.info(f'switched to "{mode}"')
        except Exception as em:
            self.logger.error(f'failed to switch to {mode}: {em}')

        sleep(interval)

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

    # RETURNS HEADERS AND URL
    def __getitem__(self, key):
        return self.headers
    
    def get_live_price(self, instruments: list):
        """
        :param instruments:
        :return:
        """
        payload = {
        }
        for instrument in instruments:
            payload.update(dict({"ticker": instrument, "useAskPrice": "false"}))
        r = requests.get(f'{self.url}/charting/v1/watchlist/batch/deviations', headers=self.headers,
                         data=[json.dumps(payload)])

    # GET AUTH VALIDATE
    def auth_validate(self) -> dict:
        """

        :return: {'id': '********-****-****-****-************', 'accountId': ********, 'customerId': ********,
        'tradingType': 'CFD', 'customerUuid': '********-****-****-****-************', 'frontend': 'WC4',
        'readyToTrade': True, 'deviceUuid': ''}
        """
        r = requests.get(f'{self.url}/auth/validate', headers=self.headers)
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
        r = requests.get(f'{self.url}/rest/v1/accounts', headers=self.headers)
        return r.json()

    # GET ACCOUNT FUNDS
    def get_funds(self) -> dict:
        """Get account funds

        :return: dict={'20434246': {'accountId': ********,
        'tradingType': 'CFD', 'currency': 'GBP', 'freeForWithdraw': 310.5,
        'freeForCfdTransfer': 0, 'total': 4954.12, 'lockedCash': {'totalLockedCash': 0, 'lockedCash': []}}}
        """
        r = requests.get(f"{self.url}/rest/v2/customer/accounts/funds", headers=self.headers)
        return r.json()

    # GET ORDER SIZE
    def get_max_min(self, instrument) -> dict:
        """Get the min and max 'BUY' & 'SELL' for an instrument passed to this function.
        :param instrument:
        :return: {'minBuy': 1.0, 'maxBuy': 4593.17,
        'minSell': 1.0, 'maxSell': 0.0, 'sellThreshold': 0.0, 'maxSellQuantity': 0}
        """
        params = {'instrumentCode': {instrument}}
        r = requests.get(f"{self.url}/v1/equity/value-order/min-max",
                         headers=self.headers,
                         params=params)
        return r.json()

    # CANCEL ORDER
    def cancel_order(self, order_id) -> dict:
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
        r = requests.delete(url=f"{self.url}/rest/v2/pending-orders/entry/{order_id}",
                            headers=self.headers, data=json.dumps(payload))
        return r.json()
    
    # CANCEL ALL PENDING ORDERS
    def cancel_all_orders(self) -> dict:
        """"""
        payload = []
        data = requests.post(url=f"{self.url}/rest/trading/v1/accounts/summary",
                             headers=self.headers, data=json.dumps(payload))

        r = requests.delete(url=f"{self.url}/rest/v2/pending-orders/cancel",
                            headers=self.headers, data=data)

        return r.json()

    # CANCEL ORDER
    def close_position(self, position_id, quantity, current_price) -> dict:
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

        r = requests.delete(url=f"{self.url}/rest/v2/trading/open-positions/close/{position_id}",
                            headers=self.headers, data=json.dumps(payload))
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

        r = requests.post(url=f"{self.url}/rest/trading/v1/accounts/summary", headers=self.headers,
                          data=json.dumps(payload))

        return r.json()

    # GET LIST OF COMPANIES
    def get_companies(self) -> list:
        """
        This function will return a list of tickers and their corresponding isin code.
        :return: [{'ticker': 'TICK', 'isin': '*************'}]
        """

        r = requests.get(f"{self.url}/rest/companies", headers=self.headers)

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
        r = requests.get(f'{self.url}/v2/instruments/additional-info/{instrument}',
                         headers=self.headers)

        return r.json()

    # GET INSTRUMENT INFORMATION
    def get_order_info(self, instrument: str, quantity):
        """

        :param instrument:
        :param quantity:
        :return:
        """
        params = {'instrumentCode': f"{instrument}",
                  'quantity': quantity,
                  'positionId': 'null'}

        r = requests.get(f"{self.url}/rest/v1/tradingAdditionalInfo", headers=self.headers, params=params)

        return r.json()

    # GET ASK PRICE FOR INSTRUMENT
    def get_ask(self, instrument: str, _useaskprice: str = "false") -> list:
        """

        :param instrument:
        :param _useaskprice:
        :return: [{'request': {'ticker': '****', 'useAskPrice': False}, 'response':
        {'timestamp': 1687852810000, 'price': 250.37, 'period': 'd1'}}]
        """

        payload = [{"ticker": f"{instrument}", "useAskPrice": f"{_useaskprice}"}]

        r = requests.put(f'{self.url}charting/v1/watchlist/batch/deviations',
                         headers=self.headers, data=json.dumps(payload))

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

        r = requests.post(f'{self.url}/rest/v2/pending-orders/entry-dep-limit-stop/{instrument}',
                          headers=self.headers,
                          data=json.dumps(payload))

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

        r = requests.post(url=f"{self.url}/rest/v2/trading/open-positions",
                          headers=self.headers, data=json.dumps(payload))

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

        r = requests.put(f"{self.url}/rest/v2/pending-orders/associated/{position_id}",
                         headers=self.headers, data=json.dumps(payload))

        return r.json()

    # RESET DEMO ACCOUNT
    def _reset(self, account_id: int, amount: int, currency_code: str):
        """"""
        payload = {"accountId": account_id, "amount": amount, "currencyCode": f"{currency_code}", "reason": "settings"}

        r = requests.post(f"{self.url}/rest/v1/account/reset-with-sum", headers=self.headers, data=json.dumps(payload))

        return r
