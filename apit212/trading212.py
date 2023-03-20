# Unofficial trading212 API
# Author: Flock92

import pickle
import asyncio
import datetime
import threading
from helpers import *
from constant import *
from functools import wraps
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.common.exceptions import *
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

#HANDLE USER FUNCTIONS
class Coro:
    pass

#WRAP FUNCTIONS ADD TO Coro CLASS
def coro(frame):
    def decorator(signum, frame):
        @wraps(frame)
        def wrapper(*args, **kwargs):
            return frame(*args, **kwargs)
        setattr(Coro, frame.__name__, wrapper)
        return frame
    return decorator

#RESTART FAILED DRIVER
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

#PRESET DRIVER SETUPS
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
    
#MAIN CLASS ()
class Client(object):
    def __init__(self, options):
        self.whole=options
        self.options=options[0]
        self.browser=options[1]
        self.headless=options[2]
    def run(
            self, 
            user: str = None, 
            access: str = None, 
            platform: str = 'PRACTICE', 
            speed: float = 0.5, 
            sleep_time: float = 15, 
            save_cookies: bool = False,
            reconnect: bool = True):
        
        #setup driver
        fulloption = self.whole
        options = self.options
        browser = self.browser
        headless = self.headless

        if browser == "chrome": self.driver: webdriver.Chrome = webdriver.Chrome(options=options)
        elif browser == "edge": self.driver: webdriver.Edge = webdriver.Edge(options=options)

        self.driver.maximize_window()
        self.driver.get(URL)
   
        setup = Setup(self.driver)
        action = Elem(self.driver)
        reboot = Reboot(self.driver, fulloption)
        monitor = Monitor(self.driver)

        #check if driver has connected to the site
        try: 
            check = self.driver.current_url
            if check != URL: em = f'failed to connect to {URL}', reboot.restart(em, "URL")
            if check == URL: print(f'connected to {URL}')
        except Exception as em:
            print(f"exception caught: {type(em)} {em}")
        
        #check if site denied access and log
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

        #check for cookies files
        file_exist = os.path.exists('cookies.pkl')
        if (reconnect == True) and (file_exist == True):
            try:
                cookies = pickle.load(open("cookies.pkl", "rb"))
                for cookie in cookies:
                    self.driver.add_cookie(cookie)
                self.driver.get(URL)
            except Exception as em:
                pass
        else:
            pass

        sleep(sleep_time)
        #start login
        setup.login(user, access, reconnect, headless)

        #unsupported driver error handler
        try:
            unsupported = self.driver.find_element(By.XPATH,f"{UNSUPPORTED}")
        except Exception as em:
            unsupported = False
            pass
        if unsupported == True:
            print(f"driver shutdown: {unsupported.text}")
            self.driver.quit()
            quit()
        else:
            pass

        #close popup for new accounts ("for users who create accounts to try this API")
        sleep(sleep_time)
        try:
            self.driver.find_element(By.XPATH,f"{CLOSE}")
            if headless == True: action.click(xpath=CLOSE, msg="popup") 
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}: close_popup")
        try:
            self.driver.find_element(By.XPATH,f"{CLOSE}")
            if headless == False: action.script_click(xpath=CLOSE, msg="popup")
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}: close_popup")
        
        #check page successfully logged in
        sleep(sleep_time)
        while True:
            try:
                verified = self.driver.find_element(By.XPATH,f"{USER_NAME}")
                print(f"login verified: {verified.text}")
                break
            except Exception as em:
                print(f"exception caught: {type(em)}: {em}")
                reboot.restart(msg="account not verified", error="USER")
        
        #save cookies
        if reconnect == True:
            try:
                pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))
            except Exception as em:
                print(f"exception caught: {type(em)}: {em}")
        else:
            pass

        #check trading account (switch between practice and real)
        setup.switch(platform)

        #setup position table (use once an order has been made)
        setup.set_POS()

        #start threads to monitor account
        #t1 = threading.Thread(target=monitor.account)
        t2 = threading.Thread(target=monitor.positions)
        t3 = threading.Thread(target=monitor.login_ex)
        #t1.daemon = True
        t2.daemon = True
        t3.daemon = True
        #t1.start()
        t2.start()
        t3.start()

        #start users script
        asyncio.run(event_loop(self.driver))
        pause = input("Press Enter to exit. . .")
        try:
            self.driver.stop_client()
            self.driver.close()
            self.driver.quit()
            quit()
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
    
    #Users functions
    @coro
    def event(signum, frame):
        pass

#RUN USER SCRIPT
async def event_loop(driver):
    loop = asyncio.get_event_loop()
    f1 = loop.create_task(Coro.monitor_account())
    f2 = loop.create_task(Coro.trade(driver))
    f3 = loop.create_task(Coro.trade2(driver))
    task = await asyncio.wait([f1,f2,f3])
    loop.run_forever()
    #loop.close()

class Trade:
    def __init__(self, driver):
        self.value = driver
    def CFD_trade(self, symbol: str, instrument_name: str, trade: str, set_percent:float=None, sleep_time: float=1):
        drive = self.value
        action = Elem(drive)
        math = Algo
        monitor=Monitor(drive)
        #get account value
        try:
            account_value = monitor.get_account_value("account_value")
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
        #MAKE SURE TRADE WINDOWS ON MARKET ORDER
        try:
            action.click(MARKET_ORDER)
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
        #OPEN MENU FOR NEW ORDERS & INPUT TICKER SYMBOL
        try:
            action.click(NEW_ORDER)
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
        try:
            item = drive.find_element(By.XPATH,f'{SEARCH_INPUT_BAR}')
            item.clear()
            item.send_keys(symbol)
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
        #FIND ITEM FROM LIST AND VERIFY BY COMPARING COMPANY NAME.
        try:
            sleep(sleep_time)
            list_items = drive.find_elements(By.XPATH,f'{LIST0}/descendant::div[@class="search-results-instrument"]')#data-qa-code search-results-instrument
            for i in list_items:
                txt = i.text
                if instrument_name in txt:
                    i.click()
                    break
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
        #SELECT TRADE TYPE
        if trade == "BUY":
            try:
                action.click(BUY_BUTTON)
            except Exception as em:
                print(f"exception caught: {type(em)}: {em}")
        if trade == "SELL":
            try:
                action.click(SELL_BUTTON)
            except Exception as em:
                print(f"exception caught: {type(em)}: {em}") 
        #INPUT QUANTITY OF SHARES TO BUY
        sleep(sleep_time)
        #INPUT QUANTITY BASED ON PERCENTAGE of 290.82px
        #try:
        #    quantity = drive.find_element(By.XPATH,f'{QUANTITY_SLIDER_RIGHT}').click()
        #except Exception as em:
        #    print(f"exception caught: {type(em)}: {em}")
        try:
            current_quantity_text = drive.find_element(By.XPATH,f"{QUANTITY}").text
            current_quantity = ''.join(c for c in current_quantity_text if c not in '£,')
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
        try:
            current_price_text= drive.find_element(By.XPATH,f"{ORDER_COST}").text
            current_price = ''.join(c for c in current_quantity_text if c not in '£,')
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
        order_quantity = math.limit_order_By_percent(
            current_quantity, 
            current_price, 
            account_value, 
            set_percent)
        try:
            quan_button = drive.find_element(By.XPATH,F"{QUANTITY_BUTTON}")
            current_input = quan_button.text
            quan_input = drive.find_element(By.XPATH,f"{QUANTITY}")
            quan_input.click()
            for i in current_input:
                quan_input.send_keys(Keys.BACK_SPACE)
            quan_input.send_keys("value", order_quantity)
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")

        #SET STOPLOSS
        try:
            action.click(SL, msg="stop loss")
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
        #SET TAKEPROFIT
        try:
            action.click(TP, msg="take profit")
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
        #SCROLL DOWN AND SET TP AND SL AMOUNT ------------------------------------------------------------------ FIX
        try:
            scroll = drive.find_element(By.XPATH,f"{SCROLL_ORDER_MENU}")
            drive.execute_script("arguments[0].setAttribute('style', 'top:182px;')", scroll)                         #184.871
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
        try:
            sleep(sleep_time)
            tp_amount = drive.find_element(By.XPATH,f"{SET_TP_AMMOUNT}")
            action.rme_input(drive, SET_TP_AMMOUNT)
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
        try:
            sleep(sleep_time)
            tp_amount = drive.find_element(By.XPATH,f"{SET_SL_AMMOUNT}")
            action.rme_input(drive, SET_SL_AMMOUNT)
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
        #COMFIRM ORDER
        try:
            action.click(CONFIRM_ORDER)
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
            
    #CLOSE NAME POSITION (PROFIT OR LOSS)
    def CFD_close(self, name: str, distance: float):
        drive = self.value
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
            sleep()
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
    async def CFD_add_list(self, _symbols):
        drive = self.value
        chart_tabs = drive.find_elements(By.XPATH,f'{CHART_TABS}/descendant::div[@class="trading-chart-tab-item-container"]')
        tab = chart_tabs
        action= Elem
        print(tab)
        sleep(2)
        symbol_list = _symbols
        n = 0
        for i in symbol_list:
            n = n
            try:
                #add_ticker = driver.find_element(By.XPATH,f"{ADD_TICKER}")
                #add_ticker.click()
                action.try_click(drive, ADD_TICKER2, ADD_TICKER, 1,3,"add ticker layout")
                try:
                    item = drive.find_element(By.XPATH,f'{SEARCH_INPUT_BAR}')
                    item.clear()
                    item.send_keys(i)
                    name = i
                    sleep(3)
                    try:
                        action.select(name, drive)
                        n = n + 1
                        sleep(2)
                    except Exception as em:
                        print(em)
                except Exception as em:
                    print(em)
            except Exception as em:
                print(em)
    #SET RULES TO CLOSE OPEN POSISTIONS
    #0 = instrument / 1 = Quantity / 2 = Driection / 3 = price / 4 = Current_price / 5 = TP / 6 = SL / 7 = Margin / 8 = Result
    def CFD_close_open(
            self, 
            sell_price: 
            float = 1, 
            sleep_time: 
            float=1.0):
        drive = self.value
        print("close CFD started")
        try:
            list_items = drive.find_elements(By.XPATH,f'{OPEN_POSISTION_LIST}/descendant::div[@class="positions-table-item"]') #/descendant::div[@class="positions-table-item"]
        except Exception as em:
            print(f"exception caught: {type(em)}: {em}")
            drive.refresh()
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
                    try:
                        close = drive.find_element(By.XPATH,f"{CLOSE_BUTTON_MENU}").click()
                        #elem.click(drive, CLOSE_BUTTON_MENU, 1,3,f"close position {instrument}")
                    except Exception as em:
                        print(f"exception caught: {type(em)}: {em}")
                    try:
                        confirm = drive.find_element(By.XPATH,f"{CONFIRM_CLOSE}").click()
                        #elem.click(drive, CLOSE_POSITION, 1, 3,f"confirm close {instrument} @ {current_price}")
                    except Exception as em:
                        print(f"exception caught: {type(em)}: {em}")
                    #try:
                    #    home = drive.find_element(By.XPATH,f"{HOME}").click()
                    #except Exception as em:
                    #    print(em)
                    #try:
                    #    home = drive.find_element(By.XPATH,f"{HOME3}").click()
                    #except Exception as em:
                    #    print(em)
                    #try:
                    #    home = drive.find_element(By.XPATH,f"{HOME4}").click()
                    #except Exception as em:
                    #    print(em)
                    print(f'closed {position}')

                else:
                    pass
