import os
import getpass
from constant import *
from time import sleep
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from constant import LIVE_RESULTS as LR, FREE_FUNDS as FF, BLOCKED_FUNDS as BF, ACCOUNT_STATUS as AS

#SHARED DATA
class Data():
    def __init__(self, *kwargs):
        self.value = kwargs
    def getPositions(self):
        for i in self.value:
            print(i)
    def getaccount(self):
        return self.value
        
#MONITOR ACCOUNT RUN THREADING 
class Monitor:  
    def __init__(self, driver, **kwargs):
        self.value = driver
    def account(self, value: tuple = [LR, FF, BF, AS], on: bool = True, sleep_time: float = 1):
        driver = self.value
        passData=Data
        while on == True:
            try: 
                live_results = driver.find_element(By.XPATH,f"{LR}").text
                num1 = live_results
                num1 = ''.join(c for c in num1 if c not in '£,')
                Live_Results = float(num1)
            except AttributeError as em:
                pass
            except InvalidSessionIdException as em:
                pass
            except TimeoutException as em:
                pass
            except NoSuchElementException as em:
                pass
            except StaleElementReferenceException as em:
                pass
            except UnboundLocalError as em:
                pass
            try: 
                free_funds = driver.find_element(By.XPATH,f"{FF}").text
                num2 = free_funds
                num2 = ''.join(c for c in num2 if c not in '£,')
                Free_Funds = float(num2)
            except AttributeError as em:
                pass
            except InvalidSessionIdException as em:
                pass
            except TimeoutException as em:
                pass
            except NoSuchElementException as em:
                pass
            except StaleElementReferenceException as em:
                pass
            except UnboundLocalError as em:
                pass
            try: 
                blocked_funds = driver.find_element(By.XPATH,f"{BF}").text
                num3 = blocked_funds
                num3 = ''.join(c for c in num3 if c not in '£,')
                Blocked_Funds = float(num3)
            except AttributeError as em:
                pass
            except InvalidSessionIdException as em:
                pass
            except TimeoutException as em:
                pass
            except NoSuchElementException as em:
                pass
            except StaleElementReferenceException as em:
                pass
            except UnboundLocalError as em:
                pass
            try: 
                account_status = driver.find_element(By.XPATH,f"{AS}").text
                num4 = account_status.split(' ')
                num4 = num4[1]
                num4 = ''.join(c for c in num4 if c not in '%')
                Account_Status = int(num4)
            except AttributeError as em:
                pass
            except InvalidSessionIdException as em:
                pass
            except TimeoutException as em:
                pass
            except NoSuchElementException as em:
                pass
            except StaleElementReferenceException as em:
                pass
            except UnboundLocalError as em:
                pass
            result = {'liveResults':Live_Results,'freeFunds':Free_Funds,'blockedFunds':Blocked_Funds,'accountStatus':Account_Status}
            passData(result)
            sleep(sleep_time)       
    def positions(self, value: tuple = [], on: bool = True):
        driver = self.value
        passData=Data
        while on == True:
            try:
                list_items = driver.find_elements(By.XPATH,f'{OPEN_POSISTION_LIST}/descendant::div[@class="positions-table-item"]') #/descendant::div[@class="positions-table-item"]
            except AttributeError as em:
                print(f"exception caught: {em}")
            except InvalidSessionIdException as em:
                print(f"exception caught: {em}")
            except StaleElementReferenceException as em:
                print(f"exception caught: {em}")
            except NoSuchElementException as em:
                print(f"exception caught: {em}")
                driver.refresh()
            #0 = instrument / 1 = Quantity / 2 = Driection / 3 = price / 4 = Current_price / 5 = TP / 6 = SL / 7 = Margin / 8 = Result
            sleep(2)
            n = 0
            for i in list_items:
                    n = n + 1
                    txt = i.text
                    option = txt.split()
                    instrument = option[0]
                    position_num = option[1]
                    quantity = option[2]
                    quantity_strip = quantity.replace(',','')
                    quantity_num = quantity_strip
                    bought_price = option[5]
                    current_price = option[6]
                    direction = option[3]
                    result = option[-1]
                    current_result = float(result)
                    #posistion 1: f'USDGBP', USD/GBP, POS1014539043, 5,000, BUY, -7.50 (liverun print)
                    #
                    dictobj = {"posistion":f"{position_num}","price":f"{bought_price}","instrument":f"{instrument}","quantity":quantity_num,"current_price":f"{direction}","result":current_result,"element":i}
                    #print(dictobj)

                    item_list = {'instrument':f"{instrument}",'quantity':quantity_num,'current_price':f"{bought_price}",'result':current_result}
                    #print(f'{item_list}\n')
                    passData(dictobj)
                    #passData.position=position_num
                    #passData.value=item_list

                    #json_obj = {"instrument":f"{instrument}","posistion":f"{position_num}","quantity":quantity_num,"current_price":f"{direction}","result":num}
                    #position = f"posistion {n}: f'{instrument}', {quantity}, {direction}, {pric}, {current_price}, {result}"
                    #print(position)
                    #with open('posistion_data.json', 'w') as outfile:
                    #    json.dump(json_obj, outfile)
    def login_ex(self, sleep_time: float = 1, on: bool = True):
        #sign back in if page expires
        driver = self.value
        while on == True:
            try: 
                log_in = driver.find_element(By.XPATH,f"{LOG_IN}")
                log_in.click()
            except Exception as em:
                pass
            #if log_in == True: log_in.click()
            sleep(sleep_time)
            
#HANDLE FILES
class File:
    def delete_file(self, file_name):
        location = print(os.path.expanduser('~'))
        if os.path.exists(f"{file_name}"):
            os.remove(f"file_name")
        else:
            pass
    def val2json(self, file_name, new_value, location):
        if new_value == None:
            msg = "no value avaliable to proccess"
            return 
            
#ELEMENT INTERACTION
class Elem:
    def __init__(self, driver):
        self.value = driver
    def click(self, xpath, speed: float = 0.3, timeout: int = 3, msg: str = "element clicked"):
        driver = self.value
        count = 0
        while count < timeout:
            try:
                elem = driver.find_element(By.XPATH,f"{xpath}")
                elem.click()
                print(f"successful click: {msg}")
                sleep(speed)
                break
            except AttributeError as em:
                count += 1
                if count == timeout: print(f"timeout!\t{msg}.{em}")
            except NoSuchElementException as em:
                count += 1
                if count == timeout: print(f"timeout!\t{msg}.{em}")
            except ElementNotInteractableException as em:
                count += 1
                if count == timeout: print(f"timeout!\t{msg}.{em}")
            except StaleElementReferenceException as em:
                count += 1
                if count == timeout: print(f"timeout!\t{msg}.{em}")
    def script_click(self, xpath, speed: float = 0.3, timeout: int = 3, msg: str = "element clicked"):
        driver = self.value
        count = 0
        while count < timeout:
            try:
                elem = driver.find_element(By.XPATH, xpath)
                driver.execute_script("arguments[0].click();", elem)
                print(f"successful scripted click: {msg}")
                sleep(speed)
                break
            except AttributeError as em:
                count += 1
                if count == timeout: print(f"timeout!\t{msg}.{em}")
            except NoSuchElementException as em:
                count += 1
                if count == timeout: print(f"timeout!\t{msg}.{em}")
            except ElementNotInteractableException as em:
                count += 1
                if count == timeout: print(f"timeout!\t{msg}.{em}")
            except StaleElementReferenceException as em:
                count += 1
                if count == timeout: print(f"timeout!\t{msg}.{em}")
    def try_click(self, xpath: tuple =[] , speed: float = 0.3, timeout: int = 3, msg: str = "element clicked"):
        driver = self.value
        count = 0
        while count < timeout:
            for i in xpath:
                try:
                    l = driver.find_element(By.XPATH,f"{xpath[count]}")
                    l.click()
                    print(f"successful click: {msg}")
                    break
                except AttributeError as em:
                    count += 1
                    if count == timeout: print(f"timeout!\t{msg}.{em}")
                except NoSuchElementException as em:
                    count += 1
                    if count == timeout: print(f"timeout!\t{msg}.{em}") 
    def input_byname(self, elem_name, value, speed: float = 0.3):
        driver = self.value
        if value == None:
            if elem_name == "password":
                value = getpass.getpass(f"{elem_name}: ")
            else:
                value = input(f"{elem_name}: ")
        try:
            input_value = driver.find_element(By.NAME,f"{elem_name}")
            input_value.send_keys(value) 
            if input_value == input.text: return f"successful input @ {elem_name}"
            sleep(speed)
        except AttributeError as em:
            return em
        except NoSuchElementException as em:
            return em
    def rme_input(self,xpath):
        driver = self.value
        field = driver.find_element(By.XPATH,f"{xpath}")
        field.click()
        current_input = field.text
        print(current_input) #testing code will need to put an function here that will base he distance on a preset percentage
        val = current_input
        for i in current_input:
            field.send_keys(Keys.BACK_SPACE)
            sleep(2)
        field.send_keys("value", val)
    def select(name, driver):
        try:
            list_items = driver.find_elements(By.XPATH,f'{LIST}/descendant::div[@class="search-results-instrument"]')#data-qa-code search-results-instrument
            print(f"started checking list {list_items}")
            for i in list_items:
                txt = i.text
                print(i.text)
                print(i)
                if name in txt:
                    try:
                        i.click()
                        print("found element")
                        break
                    except ElementClickInterceptedException as em:
                        assert(f"exception caught: {em}")
                print("\n") 
        except AttributeError as em:
            print(f"exception caught: {em}")
        except InvalidSessionIdException as em:
            print(f"exception caught: {em}")
        except TimeoutException as em:
            print(f"exception caught: {em}")
            
#SETUP TRADE ENV
class Setup:
    def __init__(self, driver):
        self.value = driver
    def check_errors(self):
        driver = self.value
    def switch(self,platform ,speed: float = 5, sleep_time: float = 3):
        driver = self.value
        print("started switch")
        current_platform = driver.find_element(By.XPATH,f"{TRADE_TYPE}").text
        value = current_platform.split(' ')
        if platform not in value:
            menu = driver.find_element(By.XPATH,f"{DROP_MENU}").click()
            sleep(sleep_time)
            if platform == "PRACTICE":
                practice = driver.find_element(By.XPATH,f"{PRACTICE}").click()
            if platform == "REAL":
                practice = driver.find_element(By.XPATH,f"{REAL}").click()
        else:
            return 0
    def set_POS(self, default: bool = True,speed: float = 1, sleep_time: float = 2):
        driver = self.value
        clicks=Elem(driver)
        try:
            adjust = driver.find_element(By.XPATH,f"{ADJUST_POS}")
            driver.execute_script("arguments[0].setAttribute('style', 'height: 165px;')", adjust)
        except NoSuchElementException as em:
            pass
        sleep(sleep_time)
        if default == True:
            try:
                clicks.click(POS_SETTINGS)
            except NoSuchElementException as em:
                pass
            except NoSuchElementException as em:
                pass    
            sleep(speed)
            try:
                clicks.click(POS_DEFAULT)
            except NoSuchWindowException as em:
                pass
            except NoSuchElementException as em:
                pass
            sleep(speed)
            try:
                clicks.click(HOME)
            except NoSuchWindowException as em:
                pass
            except NoSuchElementException as em:
                pass
            sleep(sleep_time)
            try:
                clicks.click(POS_SETTINGS)
            except NoSuchWindowException as em:
                pass 
            except NoSuchElementException as em:
                pass
            sleep(speed)
            try:
                clicks.click(POS_SL)
            except NoSuchWindowException as em:
                pass
            except NoSuchElementException as em:
                pass
            sleep(speed)
            try:
                clicks.click(POS_TP)
            except NoSuchWindowException as em:
                pass
            except NoSuchElementException as em:
                pass
            sleep(speed)
            try:
                clicks.click(POS_NUM)
            except NoSuchWindowException as em:
                pass
            except NoSuchElementException as em:
                pass
            sleep(speed)
            try:
                 clicks.click(POS_SETTINGS)
            except NoSuchWindowException as em:
                pass
            except NoSuchElementException as em:
                pass
            sleep(speed)
            try:
                driver.execute_script("arguments[0].setAttribute('style', 'height: 450px;')", adjust)
            except NoSuchElementException as em:
                pass
            except NoSuchElementException as em:
                pass
                
#MATH
class Algo:
    def percent(start_price, increase):
        base = increase/100
        num = start_price/base
        result = start_price + num
        return result


        return result
