# Unofficial trading212 API
# Author: Flock92

import os
import pickle
import asyncio
import datetime
import threading
from funcs import *
from helpers import *
from constant import *
from logs import Log
from time import sleep
from typing import Tuple
from getpass import getpass
from functools import wraps
from threading import Thread
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

#STORED USER FUNCTIONS
class Coro:
    pass 
#DINAMICALLY ADDS FUNCTION
def coro(frame):
    def decorator(signum, frame):
        @wraps(frame)
        def wrapper(*args, **kwargs):
            return frame(*args, **kwargs)
        setattr(Coro, frame.__name__, wrapper)
        return frame
    return decorator
#RESTART CLASS
class Reboot:
    def __init__(self, driver, option):
        self.value = driver
        self.build = option
    def restart(self, msg, error, sleep_time: float = 2.0):
        driver = self.value
        build = self.build
        print(f"driver restarting: {msg}")
        if error == "COOKIES": os.remove('cookies.pkl')
        driver.quit()
        sleep(10)
        start = Client(build)
        start.run()
    def hardreset(self, msg, error, sleep_time: float = 2.0):
        driver = self.value
        build = self.build
        driver.stop_client()
        driver.close()
        driver.quit()
        sleep(sleep_time)
        start = Client(build)
        start.run()
#PRE SET OPTIONS THAT CAN BE SET BUY THE USER 
class Options:
    def Chrome_default():
        ua = UserAgent()
        User = ua.random
        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--incognito")
        options.add_argument('--disable-gpu')
        options.add_argument("--disable-webgl")
        options.add_argument(f'user-agent={User}')
        options.add_argument("--window-size=1920x1080")
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        #options.add_experimental_option("excludeSwitches", ["enable-logging"])
        browser = "chrome"
        headless = False
        return options, browser, headless
    def Chrome_live_run():
        ua = UserAgent()
        User = ua.random
        options = webdriver.ChromeOptions()
        options.headless = False
        options.add_argument("--incognito")
        options.add_argument('--disable-gpu')
        options.add_argument(f'user-agent={User}')
        options.add_argument("--window-size=1920x1080")
        #options.add_argument("user-data-dir=C:\\User\\Username\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data")
        options.add_argument("--remote-debugging-port=9230")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        browser = "chrome"
        headless = True
        return options, browser, headless
    def Edge_default():
        ua = UserAgent()
        User = ua.random
        options = webdriver.EdgeOptions()
        options.headless = True
        options.add_argument("--incognito")
        options.add_argument('--disable-gpu')
        options.add_argument(f'user-agent={User}')
        options.add_argument("--window-size=1920x1080")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("detach",True)
        browser = "edge"
        headless = True
        return options, browser, headless
    def Edge_live_run():
        ua = UserAgent()
        User = ua.random
        options = webdriver.EdgeOptions()
        options.headless = False
        options.add_argument("--incognito")
        options.add_argument('--disable-gpu')
        options.add_argument(f'user-agent={User}')
        options.add_argument("--window-size=1920x1080")
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        browser = "edge"
        headless = False
        return options, browser, headless
#MAIN FUNCTION
class Client(object):
    def __init__(self, options):
        self.value = options
    #STARTS UP DRIVERS AND LOGS INTO PRESET ACCOUNT
    def run(self, user: str = None, access: str = None, platform: str = 'PRACTICE', speed: float = 0.5, sleep_time: float = 15, *,reconnect: bool = True):
        options = self.value[0]
        browser = self.value[1]
        headless = self.value[2]
        rebootop = self.value
        global drive

        #START DRIVER
        if browser != "chrome": self.driver: webdriver.Edge = webdriver.Edge(options=options)
        if browser == "chrome": self.driver: webdriver.Chrome = webdriver.Chrome(options=options)

        drive = self.driver

        sessionID = self.driver.session_id
        cap = self.driver.capabilities.copy()
        print(cap)
        print(sessionID)

        #FULL SCREEN 
        self.driver.maximize_window()

        #CONNECT TO SITE
        self.driver.get(URL)

        #SEND VALUE TO MODULE CLASSES
        delFile = File()
        action = Elem(self.driver)
        monitor = Monitor(self.driver)
        reboot = Reboot(self.driver, rebootop)
        setup = Setup(self.driver)
        #log = Log()

        #CHECK CONNECTION
        try: 
            check = self.driver.current_url
            if check != URL: em = f'failed to connect to {URL}', reboot.restart(em, "URL")
            if check == URL: print(f'connected to {URL}')
        except AttributeError as em:
            print(f"exception caught: {em}")

        #CHECK IF DENIED ACCESS
        try:
            access_denied = self.driver.find_element(By.XPATH,f"{ACCESS_DENIED}")
            blocked_ip = self.driver.find_element(By.XPATH,f"{ACCESS_DENIED_IP}")
            to_file = f"T212 DENIED ACCESS:\tIP:{blocked_ip.text}"
            if access_denied == True:
                with open('log.txt', 'a', newline='') as errorfile:
                    errorfile.write(to_file)
                reboot.hardreset(to_file, "access denied")
        except:
            pass

        #CHECK FOR COOKIES / ADDING COOKIES FOR AUTO LOGIN
        file_exist = os.path.exists('cookies.pkl')
        if (reconnect == True) and (file_exist == True):
            try:
                cookies = pickle.load(open("cookies.pkl", "rb"))
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                self.driver.get(URL)
            except FileNotFoundError as em:
                print(f"exception caught: {em}")
                pass
        sleep(sleep_time)

        #START LOGIN IF AUTO LOGIN FAILS
        check = self.driver.current_url
        if check == URL:
            sleep(sleep_time)
            try:
                action.script_click(xpath=COOKIES, msg="cookies popup")
            except AttributeError as em:
                print(f"exception caught: {em} cookies")
            try:
                login = self.driver.find_element(By.XPATH,f"{LOGIN}")
                action.click(xpath=LOGIN)
            except AttributeError as em:
                print(f"exception caught: {em} login")
            self.driver.implicitly_wait(speed)

            #INPUT USERNAME AND PASSWORD
            try:
                action.input_byname("email", user)
            except AttributeError as em:
                print(f"exception caught: {em} email input")
            except NoSuchElementException as em:
                print(f"exception caught: {em} email input")
            try:
                action.input_byname("password", access)
            except AttributeError as em:
                print(f"exception caught: {em} password input")
            except NoSuchElementException as em:
                print(f"exception caught: {em} password input")
            if reconnect == False:
                print('reconnect is false: cookies will not be saved')
                try:
                    action.click(xpath=MEM_BUTTON, msg="mem button")
                except AttributeError as em:
                    print(f"exception caught: {em} mem button")
                except NoSuchElementException as em:
                    print(f"exception caught: {em} mem button")
            else:
                print("reconnect is true: cookies will be saved")
            try:
                action.click(xpath=SUBMIT, msg="submit")
            except AttributeError as em:
                print(f"exception caught: {em} submit")
            except NoSuchElementException as em:
                print(f"exception caught: {em} submit")
            sleep(sleep_time)
        else:
            sleep(sleep_time)

        #RARE ERRORS HANDLING
        try:
            unsupported = self.driver.find_element(By.XPATH,f"{UNSUPPORTED}")
            unsupported_msg = 'Your current browser is not supported'
            if unsupported_msg in unsupported.text:
                print(f"driver shutdown: {unsupported_msg}")
                self.driver.quit()
                quit()
                #reboot.hardreset(unsupported_msg, "unsupported driver")
            else:
                pass
        except AttributeError as em:
            pass
        except NoSuchWindowException as em:
            pass
        except NoSuchElementException as em:
            pass

        #CLOSE POP UP MENUE (NOT ALWAYS PRESENT)
        sleep(sleep_time)
        try:
            self.driver.find_element(By.XPATH,f"{CLOSE}")
            if headless == True: action.click(xpath=CLOSE, msg="popup") 
        except AttributeError as em:
            pass
        except NoSuchWindowException as em:
            pass
        except NoSuchElementException as em:
            pass
        try:
            self.driver.find_element(By.XPATH,f"{CLOSE}")
            if headless == False: action.script_click(xpath=CLOSE, msg="popup")
        except AttributeError as em:
            pass
        except NoSuchWindowException as em:
            pass
        except NoSuchElementException as em:
            pass

        #CHECK PAGE TO CONFIRM SUCCESSFUL LOGIN
        sleep(sleep_time)
        while True:
            try:
                verified = self.driver.find_element(By.XPATH,f"{USER_NAME}")
                print(f"login verified: {verified.text}")
                break
            except AttributeError as em:
                print(f"exception caught: {em}")
                reboot.restart(em, "UNVERIFIED")
            except NoSuchElementException as em:
                print(f"exception caught: {em}")
                reboot.restart(em, "UNVERIFIED")
            except NoSuchWindowException as em:
                assert(f"exception caught: {em}")
                self.driver.quit   

        #SAVE COOKIES
        if reconnect == True:
            print("saving cookies:")
            try:
                pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
            except:
                print("cookie file not saved")    
        else:
            print("reconnect: False")

        #SWITCH BETWEEN PRACTICE AND
        setup.switch(platform)

        sleep(sleep_time)
        #SET POSISTION TABLE based on the amount of open trades
        setup.set_POS()

        #START SCRIPT TO MONITOR ACCOUNT.
        t1 = threading.Thread(target=monitor.account)
        t2 = threading.Thread(target=monitor.positions)
        t3 = threading.Thread(target=monitor.login_ex)
        t1.daemon = True
        t2.daemon = True
        t3.daemon = True
        t1.start()
        t2.start()
        t3.start()

        asyncio.run(event_loop())
        pause = input("Press Enter to exit. . .")
        try:
            self.driver.stop_client()
            self.driver.close()
            self.driver.quit()
            quit()
        except InvalidSessionIdException as em:
            print(f"exception caught: {em}")
    #USER PASSES FUNCTIONS
    @coro
    def event(signum, frame):
        pass
#RUN USER SCRIPT
#async def event_loop():
#    print("function started. . .")
#    asyncio.run(Coro.monitor_account())
    #await asyncio.gather(
    #      Coro.monitor_account(),
    #      Coro.trade(),
    #      Coro.trade2()
    #)

async def event_loop():
    print("loop started")
    loop = asyncio.get_event_loop()
    try:
            task1 = asyncio.ensure_future(Coro.monitor_account())
            task2 = asyncio.ensure_future(Coro.trade())
            task3 = asyncio.ensure_future(Coro.trade2())
            loop.run_forever(task1, task2, task3)
    except KeyboardInterrupt:
        pass
    finally:
        return 0
    
#async def event_loop():
#    loop = asyncio.get_event_loop()
#    f1 = loop.create_task(Coro.monitor_account())
#    f2 = loop.create_task(Coro.trade())
#    f3 = loop.create_task(Coro.trade2())
#    await asyncio.wait([f1,f2])
#    loop.run_until_complete()
#    loop.close()

def printme():
    print("called this function")
    

def CFD_trade(symbol: str, instrument_name: str, trade: str, quantity:float=None, Pquantity:float=None, sleep_time: float=1):
    print("CFD_TRADE STARTED")
    action = Elem(drive)
    #OPEN MENU FOR NEW ORDERS & INPUT TICKER SYMBOL
    try:
        order_menu = drive.find_element(By.XPATH,f'{NEW_ORDER}')
        order_menu.click()
        drive.implicitly_wait(1)
    except Exception as em:
        print(f"order menu: {em}")
    try:
        drive.implicitly_wait(1)
        item = drive.find_element(By.XPATH,f'{SEARCH_INPUT_BAR}')
        item.clear()
        item.send_keys(symbol)
    except Exception as em:
        print(f"search input: {em}")
    #FIND ITEM FROM LIST AND VERIFY BY COMPARING COMPANY NAME.
    try:
        sleep(1)
        list_items = drive.find_elements(By.XPATH,f'{LIST0}/descendant::div[@class="search-results-instrument"]')#data-qa-code search-results-instrument
        print(f"started checking list: {list_items}")
        for i in list_items:
            txt = i.text
            print(txt)
            if instrument_name in txt:
                i.click()
                break
            print("\n") 
    except Exception as em:
        print(f"list items: {em}")
    #SELECT TRADE TYPE
    if trade == "BUY":
        try:
            buy = drive.find_element(By.XPATH,f'{BUY_BUTTON}')
            buy.click()
        except Exception as em:
            print(f"BUY button: {em}")
    if trade == "SELL":
        try:
            sell = drive.find_element(By.XPATH,f'{SELL_BUTTON}')
            sell.click()
        except Exception as em:
            print(f"SELL button: {em}")  
    #INPUT QUANTITY OF SHARES TO BUY
    sleep(1)
    #INPUT QUANTITY BASED ON PERCENTAGE of 290.82px
    try:
        quantity = drive.find_element(By.XPATH,f'{QUANTITY_SLIDER_RIGHT}').click()
    except Exception as em:
        print(f"quantity_right_button: {em}")
    try:
        quan_button = drive.find_element(By.XPATH,f"{QUANTITY}")
        current_input = quan_button.text
        print(current_input)
    except Exception as em:
        print(f"quantity element: {em}")
    #INPUT QUANTITY BUY SET AMMOUNT.
    ##try:
    ##    quan_button = drive.find_element(By.XPATH,F"{QUANTITY_BUTTON}")
    ##    current_input = quan_button.text
    ##    quan_input = drive.find_element(By.XPATH,f"{QUANTITY}")
    ##    quan_input.click()
    ##    for i in current_input:
    ##        quan_input.send_keys(Keys.BACK_SPACE)
    ##    quan_input.send_keys("value", quantity)
    ##except AttributeError as em:
    ##    print(f"exception caught: {em}")
    ##except ElementClickInterceptedException as em:
    ##    print(f"exception caught: {em}")
    ##except NoSuchElementException as em:
    ##    print(f"exception caught: {em}")
    #SET STOPLOSS
    try:
        action.click(SL, msg="stop loss")
    except Exception as em:
        print(f"stop loss button: {em}")
    #SET TAKEPROFIT
    try:
        action.click(TP, msg="take profit")
    except Exception as em:
        print(f"take profit button: {em}")
    #SCROLL DOWN AND SET TP AND SL AMOUNT ------------------------------------------------------------------ FIX
    try:
        scroll = drive.find_element(By.XPATH,f"{SCROLL_ORDER_MENU}")
        drive.execute_script("arguments[0].setAttribute('style', 'top:180px;')", scroll)                         #184.871
    except Exception as em:
        print(f"scroll: {em}")
    try:
        sleep(sleep_time)
        tp_amount = drive.find_element(By.XPATH,f"{SET_TP_AMMOUNT}")
        action.rme_input(drive, SET_TP_AMMOUNT)
    except Exception as em:
        print(f"scroll: {em}")
    try:
        sleep(sleep_time)
        tp_amount = drive.find_element(By.XPATH,f"{SET_SL_AMMOUNT}")
        action.rme_input(drive, SET_SL_AMMOUNT)
    except Exception as em:
        print(f"scroll: {em}")
    #COMFIRM ORDER
    try:
        execute = drive.find_element(By.XPATH,f"{CONFIRM_ORDER}")
        execute.click()
    except Exception as em:
        print(f"scroll: {em}")
#CLOSE NAME POSITION (PROFIT OR LOSS)
def CFD_close(name: str, distance: float):
    #close all positions when results pass a percentage
    i = 1
    while i == 1:
        try:
            list_items = drive.find_elements(By.XPATH,f'{OPEN_POSISTION_LIST}/descendant::div[@class="positions-table-item"]') #/descendant::div[@class="positions-table-item"]
            print(list_items)
            break
        except Exception as em:
            print(em)
            drive.refresh()
    try:
        sleep(2)
        for i in list_items:
                txt = i.text
                if name in txt:
                    ac = ActionChains(drive)
                    ac.context_click(i).perform()
                    while True:
                        try:
                            close_button = drive.find_element(By.XPATH,f"{CLOSE_BUTTON_MENU}")
                            close_button.click()
                            break
                        except Exception as em:
                            print(em)
                    while True:
                        try:
                            confirm = drive.find_element(By.XPATH,f"{CONFIRM_CLOSE}")
                            confirm.click()
                            break
                        except Exception as em:
                            print(em)
                    print(f"{i.text}\n position closed") #This will bring out all the information on a transcation.
    except Exception as em:
        print(em)
#ADD TO THE MAIN WATCH LIST (LATER I WILL CREATE A FUNCTION THAT MONITORS ALL THE STOCKS ON THE WATCH LIST)           
def CFD_add_list(_symbols):
    chart_tabs = drive.find_elements(By.XPATH,f'{CHART_TABS}/descendant::div[@class="trading-chart-tab-item-container"]')
    tab = chart_tabs
    print(tab)
    sleep(2)
    symbol_list = _symbols
    n = 0
    for i in symbol_list:
        n = n
        try:
            #add_ticker = driver.find_element(By.XPATH,f"{ADD_TICKER}")
            #add_ticker.click()
            elem.try_click(drive, ADD_TICKER2, ADD_TICKER, 1,3,"add ticker layout")
            try:
                item = drive.find_element(By.XPATH,f'{SEARCH_INPUT_BAR}')
                item.clear()
                item.send_keys(i)
                name = i
                sleep(3)
                try:
                    elem.select(name, drive)
                    n = n + 1
                    sleep(2)
                except Exception as em:
                    print(em)
            except Exception as em:
                print(em)
        except Exception as em:
            print(em)
#SET RULES TO CLOSE OPEN POSISTIONS
def CFD_close_open(sell_price: float = 1, sleep_time: float=1.0, on: bool = True):
    while on == True:
        try:
            list_items = drive.find_elements(By.XPATH,f'{OPEN_POSISTION_LIST}/descendant::div[@class="positions-table-item"]') #/descendant::div[@class="positions-table-item"]
            break
        except Exception as em:
            print(em)
            drive.refresh()
    #0 = instrument / 1 = Quantity / 2 = Driection / 3 = price / 4 = Current_price / 5 = TP / 6 = SL / 7 = Margin / 8 = Result
    #try:
    sleep(sleep_time)
    while True:
        for i in list_items:
                txt = i.text
                option = txt.split()
                instrument = option[0]
                quantity = option[2]
                direction = option[4]
                bought_price = option[5]
                current_price = option[6]
                result = option[-1]
                num = float(result)
                position = instrument, quantity, direction, bought_price, current_price, result
                if num > sell_price:
                    ac = ActionChains(drive)
                    ac.context_click(i).perform()
                    while True:
                        try:
                            close = drive.find_element(By.XPATH,f"{CLOSE_BUTTON_MENU}").click()
                            #elem.click(drive, CLOSE_BUTTON_MENU, 1,3,f"close position {instrument}")
                        except Exception as em:
                            print(em)
                        try:
                            confirm = drive.find_element(By.XPATH,f"{CONFIRM_CLOSE}").click()
                            #elem.click(drive, CLOSE_POSITION, 1, 3,f"confirm close {instrument} @ {current_price}")
                        except Exception as em:
                            print(em)
                        try:
                            home = drive.find_element(By.XPATH,f"{HOME}").click()
                        except Exception as em:
                            print(em)
                        try:
                            home = drive.find_element(By.XPATH,f"{HOME3}").click()
                        except Exception as em:
                            print(em)
                        try:
                            home = drive.find_element(By.XPATH,f"{HOME4}").click()
                        except Exception as em:
                            print(em)
                        print(f'closed {position}')
                        #await asyncio.sleep()
