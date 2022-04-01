from APIs.binance import Binance
from APIs.btcTurk import BtcTurk
import xlwt
import time
import json

binance = Binance('z7S1rcFYIYSfqZ8ezf3AHpY4zzwYSMNJPHPKne5qJlkllO9lebIK5vMWJRleAlWs', '0m3GlcouShoIsoFJvAhLVi9KNod2dEpEFP11TwXv0JbHT9GHPjRVt9Iee7bSOvyx')

btcturk = BtcTurk('a42db663-84df-48e9-ba57-7200093cb6ba', 'AFy2Tf/OlufIN+zTCJpiYMGbaD8nrBVA')

wb = xlwt.Workbook()
ws = wb.add_sheet("USDC_USDT")
line = 1

counter = 1

lines = ['btcTurk_bid', 'btcTurk_ask', 'binance_bid', 'binance_ask', 'time']
for i in range(len(lines)):
    ws.write(0, i, lines[i])

def unixToDate(unixDate):
    unixDate = int(unixDate)/1000 #sometimes /1000 is required for proper result
    t = time.localtime(unixDate)

    return '{}-{}-{} {}:{}:{}'.format(t.tm_mday, t.tm_mon, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec)

while True:
    try:
        btcturkStats = btcturk.ticker('USDC_USDT', timeout=2)
        binanceStats = binance.symbolOrderBookTicker('USDCUSDT', timeout=2)

        btcturkStats = json.loads(btcturkStats)['data'][0]
        binanceStats = json.loads(binanceStats)

        values = [btcturkStats['bid'], btcturkStats['ask'], binanceStats['bidPrice'], binanceStats['askPrice'], unixToDate(btcturkStats['timestamp'])]

        for value in range(len(values)):
            ws.write(line, value, values[value])

        line += 1
        wb.save('coinDatav1.xls')

        print(counter)

        counter += 1
    except:
        print('error occured.')
        
    time.sleep(2)