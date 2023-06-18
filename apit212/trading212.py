# Unofficial trading212 API
# Author: Flock92

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from getpass import getpass
from constant import *
from time import sleep, strftime
from urllib.parse import urlencode
import logging
import json


class Apit212:
    def __init__(
            self,
            username: str,
            password: str,
            timeout: int = 2,
            interval: float = 5.0,
            mode: str = 'demo'):
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

        # Check arguments passed
        allowed = ['demo', 'live']
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
            print(':param timeout: invalid input')
            quit()

        if isinstance(interval, (int, float)):
            pass
        else:
            print(':param interval: invalid input')
            quit()

        if isinstance(mode, str) and mode in allowed:
            pass
        else:
            quit(print(':param mode: invalid input "demo","live"'))
            pass

        # set variables for functions
        options = webdriver.FirefoxOptions()
        options.add_argument('--log-level=3')
        options.headless = True
        self.url = f'https://{mode}.trading212.com/'
        my_cookie = None

        # Get login details if no information was passed.
        if username is None:
            username = input('username: ')
        elif password is None:
            password = getpass('password: ')
        else:
            pass

        # Start up webdriver
        d = webdriver.Firefox(options=options)

        try:
            d.get(url=URL)
            self.logger.info(msg=f'successfully loaded {URL}')
        except Exception as em:
            self.logger.error(em)

        # if website failed to load end process.
        if d.current_url != URL:
            self.logger.error("can not verify URL"), quit(d.close())
        else:
            pass

        d.implicitly_wait(30)

        # LOGIN PROCESS
        while timeout > 0:
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

        try:
            d.get(f"https://{mode}.trading212.com")
            self.logger.info(f'switched to "{mode}"')
        except Exception as em:
            self.logger.error(f'failed to switch to {mode}: {em}')

        sleep(interval)

        cookies = d.get_cookies()

        for cookie in cookies:
            if cookie['name'] == f'TRADING212_SESSION_{mode.upper()}':
                my_cookie = f"TRADING212_SESSION_{mode.upper()}={cookie['value']};"
            else:
                pass

        user_agent = d.execute_script("return navigator.userAgent;")

        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": user_agent,
            "Cookie": f'{my_cookie}',
        }

        self.logger.info(f'finished setup...{username}')

    # GET ACCOUNT DETAILS
    def get_account(self) -> dict:
        """

        :return: json data about account info
        """
        r = requests.get(f'{self.url}/rest/v1/accounts', headers=self.headers)
        return r.json()

    # GET ACCOUNT FUNDS
    def get_funds(self) -> dict:
        """

        :return: json data of accounts funds
        """
        r = requests.get(f"{self.url}/rest/v2/customer/accounts/funds", headers=self.headers)
        return r.json()

    # GET ORDERS ID'S
    def get_order(self):
        """

        :return:
        """
        r = requests.get(url=f"{self.url}/v3/watchlists/order", headers=self.headers)
        return r.json()

    # CANCEL ORDER
    def cancel_order(self, order):
        """

        :param order:
        :return:
        """
        payload = {'positionId': f'{order}'}
        r = requests.delete(url=f"{self.url}/rest/public/v2/equity/order/{order}",
                            headers=self.headers, data=json.dumps(payload))
        return r.json()

    def get_setting(self, ticker: str) -> dict:
        """

        :param ticker:
        :return: json data
        """
        r = requests.get(f'{self.url}/v2/instruments/additional-info/{ticker}',
                         headers=self.headers)

        print(r.status_code)
        return r.json()

    def limit_order(
            self,
            ticker: str,
            quantity: int,
            target_price: int,
            take_profit: int = None,
            stop_loss: int = None,
            notify: str = 'NONE'
    ):
        """

        :param ticker:
        :param quantity:
        :param target_price:
        :param take_profit:
        :param stop_loss:
        :param notify:
        :return:
        """
        payload = {'quantity': quantity, 'targetPrice': target_price, 'takeProfit': take_profit, 'stopLoss': stop_loss,
                   'notify': notify}

        r = requests.post(f'{self.url}/rest/v2/pending-orders/entry-dep-limit-stop/{ticker}', headers=self.headers,
                          data=json.dumps(payload))

        return r.json()
