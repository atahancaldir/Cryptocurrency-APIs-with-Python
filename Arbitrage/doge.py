from APIs.binance import Binance
import json
import time
import pandas as pd

b = Binance('z7S1rcFYIYSfqZ8ezf3AHpY4zzwYSMNJPHPKne5qJlkllO9lebIK5vMWJRleAlWs',
'0m3GlcouShoIsoFJvAhLVi9KNod2dEpEFP11TwXv0JbHT9GHPjRVt9Iee7bSOvyx')

lowerLimit = 0.395
upperLimit = 0.400

while True:
    print('-'*50)

    time.sleep(20)

    doge = b.symbolPriceTicker('DOGETRY')
    doge = json.loads(doge)['price']
    doge = float(doge)

    print('doge:', doge)

    balances = b.accountInfo()
    balances = json.loads(balances)['balances']

    for balance in balances:
        if balance['asset'] == 'DOGE':
            dogeBalance = balance['free']
        elif balance['asset'] == 'TRY':
            tryBalance = balance['free']

    dogeBalance = float(dogeBalance)
    tryBalance = float(tryBalance)

    print('doge balance:', dogeBalance)
    print('try balance:', tryBalance)
    print('\ntotal money:', dogeBalance*doge + tryBalance)

    if doge<lowerLimit and tryBalance>10:
        print('\nBuying...')
        order = b.newOrder(symbol='DOGETRY', side='BUY', oType='LIMIT', timeInForce='GTC', quantity=(tryBalance/lowerLimit)-5, price=doge)

    elif doge>upperLimit and dogeBalance>100:
        print('\nSelling...')
        order = b.newOrder(symbol='DOGETRY', side='SELL', oType='LIMIT', timeInForce='GTC', quantity=dogeBalance-5, price=doge)
    
    else:
        b.cancelAllOrdersOfSymbol('DOGETRY')
        continue

    print(order)
    print('Successful')