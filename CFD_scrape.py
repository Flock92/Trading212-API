import json, time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import *
from threading import Thread

#constant variables.
URL = "https://www.trading212.com/trading-instruments/cfd"#
COOKIES = '//*[@id="__next"]/main/div/div/div[2]/div[2]/div[2]/div[1]'
LIST_FILED = '//*[@id="__next"]/main/section[2]/div/div/div[2]/div/div/div[1]/div[1]/div'
LIST_TITLES = '//*[@id="__next"]/main/section[2]/div/div/div[1]/div[2]'
SCROLL_AREA = '//*[@id="__next"]/main/section[2]/div/div/div[2]/div/div/div[2]/div'
EXPAND_TRIGGER = '//*[@id="__next"]/main/section[2]/div/div/div[2]/div/div/div[1]/div[2]/div[1]/div'
SEARCH_FIELD = '//*[@id="__next"]/main/section[2]/div/div/div[1]/div[1]/div[2]/div/div[1]/input'
SCROLL_AREA = '//*[@id="__next"]/main/section[2]/div/div/div[2]/div/div/div[1]/div[1]/div/div' #STYLE = height: 29520px; width: 100%;
SCROLL_TOP = '//*[@id="__next"]/main/section[2]/div/div/div[2]/div/div/div[2]/div' #STYLE height: 53.7805px; top: 0px; get top value

def setup(search_value):
    options = webdriver.ChromeOptions()
    options.headless=True
    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    driver.fullscreen_window()
    driver.implicitly_wait(5)
    try: driver.find_element(By.XPATH,f"{COOKIES}").click()
    except Exception as em: return f"exception caught: {type(em): {em}}"
    try: driver.find_element(By.XPATH,f"{SEARCH_FIELD}").send_keys(f"{search_value}")
    except Exception as em: print(f"exception caught: {type(em): {em}}")
    sleep(2)
    return driver
   
def get_data(search_value, sleep_time: float = 0.01):
    scrollinto = "arguments[0].scrollIntoView();"
    set_keys = {"UK":{}, "INDEX":{}, "NASDAQ":{},
                "NYSE":{}, "COMMODITIES":{}, "SWITZERLAND":{},
                "HONG KONG":{}, "OTC":{}, "FINLAND":{},
                "DENMARK":{}, "IRELAND":{}, "AUSTRIA":{},
                "PORTUGAL":{}, "RUSSIAN":{}, "SWEDEN":{},
                "POLAND":{}, "BELGIUM":{}, "NORWAY":{},
                "NETHERLANDS":{}, "SPAIN":{}, "AUSTRALIA":{},
                "FRENCE":{}, "ITALY":{}, "CANADA":{},
                "DEUTSCHE CFD":{}}
    
    if search_value not in set_keys.keys(): return f"{search_value} is not a valued arg"
    
    driver = setup(search_value)
    #Creating json file
    try:
        with open('CFD_list.json','r+',encoding=('utf-8')) as f:
            file_data = json.load(f)
            for v in set_keys:
                if v not in file_data:
                    file_data.update({f"{v}":{}})
            f.seek(0)
            json.dump(file_data,f,indent=4)
    except FileNotFoundError:
        with open('CFD_list.json','w',encoding=('utf-8')) as f:
            json.dump(set_keys,f,indent=4)

    #Save scrapped data to json file.
    
    #Get data area size
    scroll_area = driver.find_element(By.XPATH,f"{SCROLL_AREA}").get_attribute("Style")
    scroll_value = scroll_area.split(';')
    num = ''.join(c for c in scroll_value[0] if c not in 'height:px ')

    while True:
        t1 = time.perf_counter()
        try: scrapped = driver.find_elements(By.XPATH,
            f'{LIST_FILED}/descendant::div[@class="item-wrapper"]')
        except NoSuchElementException as em: break
        #Check scrapped data and end when no more new data is avalible
        try:
            if last_set == scrapped: break
        except UnboundLocalError as em:
            pass
        #Update document
        for v in scrapped:
            try: items = v.text.split('\n')
            except Exception as em: pass
            avg_spread = ''.join(c for c in items[-1] if c not in '-,£')
            if avg_spread: avg_spread = float(avg_spread)
            if not avg_spread: avg_spread = "N/A"
            try: data = {f"{items[-5]}":
                         {"name": f"{items[-6]}",
                          "isin": f"{items[-4]}",
                          "avg spread": avg_spread}}
            except IndexError as em: pass
            #Write to new file 
            with open('CFD_list.json','r+',encoding=('utf-8')) as f:
                file_data = json.load(f)
                main_key = file_data[f"{search_value}"]
                if items[-5] not in main_key:
                    file_data[f"{search_value}"].update(data)
                    f.seek(0)
                    json.dump(file_data, f, indent=4)

            last_set = scrapped
            try:
                driver.implicitly_wait(5)
                driver.execute_script(scrollinto, v)
            except StaleElementReferenceException as em:
                pass

        t2 = time.perf_counter()
    driver.close()
    return "Scrap completed"


print(get_data("DENMARK"))
