#import apit212
import asyncio
from time import sleep

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

client.run()
