from apit212 import *

username = "flock92_@account.com"
password = "password/"

client = Apit212(username=username, password=password, mode='demo')

#print(client.auth_validate())
#print(client.get_account())
#print(client.get_funds())
#print(client.get_instruments_info('TSLA'))
#print(client.get_max_min('BT'))
#print(client.limit_order('AAPL', 2, 120, 130))
#print(client.market_order('BT', 1.20, 3000))
#print(client.cancel_order(order_id)) # WILL DELETE PENDING LIMIT ORDERS WILL NEED TO GET THE POSITION ID
#print(client.get_summary()) # GET POSITION ID & PPL
