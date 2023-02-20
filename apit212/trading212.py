# Unofficial trading212 API
# Author: Flock92

import pickle
import asyncio
import threading
from log import log
from helpers import *
from time import sleep
from constant import *
from functools import wraps
from threading import Thread
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.common.exceptions import *
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
        sleep(sleep_time)
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
        #START DRIVER
        if browser != "chrome": self.driver: webdriver.Edge = webdriver.Edge(options=options)
        if browser == "chrome": self.driver: webdriver.Chrome = webdriver.Chrome(options=options)

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
        Actions(self.driver)
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
async def event_loop():
    loop = asyncio.get_event_loop()
    f1 = loop.create_task(Coro.monitor_account())
    f2 = loop.create_task(Coro.trade())
    f3 = loop.create_task(Coro.trade2())
    await asyncio.wait([f1,f2])
    loop.run_until_complete()
    loop.close()
