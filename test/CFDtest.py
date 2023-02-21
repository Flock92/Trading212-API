from main import *
import asyncio
from helpers import Data
from time import sleep
from logs import Log

options = Options.Chrome_live_run()
client = Client(options=options)


@client.event
async def monitor_account():
    data=Data()
    print(data.getaccount())
    await printme()

@client.event
async def trade():
    while True:
        await CFD_close_open()
        print("trade func 1")
        await asyncio.sleep(1)

@client.event
async def trade2():
    while True:
        print("trade func 2")
        await asyncio.sleep(1)

client.run(sleep_time=5)
