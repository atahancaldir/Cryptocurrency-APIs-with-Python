from btcTurk import BtcTurk
import pandas as pd
import json
from datetime import datetime
import time

btcturk = BtcTurk(apiKey='',
apiSecret='')

def tabularData(data, convertTime = True):
    try:
        result = pd.DataFrame(json.loads(data)['data'])
    except TypeError:
        result = pd.DataFrame(json.loads(data))
    except ValueError:
        return data

    if convertTime:
        convertible = ['timestamp', 'date', 'time', 'updateTime']

        for i in convertible:
            if i in result.columns:
                result[i] = result[i].apply(unixToDate)

    return result

def unixToDate(unixDate):
    unixDate = int(unixDate)/1000 #sometimes /1000 is required for proper result
    t = time.localtime(unixDate)

    return '{}-{}-{} {}:{}:{}'.format(t.tm_mday, t.tm_mon, t.tm_year, t.tm_hour, t.tm_min, t.tm_sec)

def dateToUnix(year, month, day):
    date = '/'.join([str(day), str(month), str(year)])
    unixDate = time.mktime(datetime.strptime(date, '%d/%m/%Y').timetuple())

    return str(int(unixDate))

result = tabularData(btcturk.ticker())
print(result)
