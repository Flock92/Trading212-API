from main import *
import asyncio
from helpers import Data
from time import sleep
from logs import Log

options = Options.Chrome_live_run()
client = Client(options=options)


@client.event
async def monitor_account():
    printme()
    return

@client.event
async def trade():
    CFD_close_open()
    print("trade func 1")
    await asyncio.sleep(1)
    return

@client.event
async def trade2():
    CFD_trade("TSLA", "Tesla", 'BUY', Pquantity=10)
    print("trade func 2")
    await asyncio.sleep(1)
    return

client.run(sleep_time=5)
