import time, base64, hmac, hashlib, requests, json
from urllib.parse import urlencode

class BtcTurk:
    def __init__(self, apiKey, apiSecret):
        self.urlBase = 'https://api.btcturk.com'
        self.apiKey = apiKey
        self.apiSecret = base64.b64decode(apiSecret)

    def requestData(self, createURL = True, requestType = 'GET', headers = {}, params = {}, timeout = None):
        if createURL:
            self.url = self.urlBase + self.urlMethod

        if requestType == 'GET':
            self.result = requests.get(url = self.url, headers = headers, json = params, timeout = None)
        elif requestType == 'POST':
            self.result = requests.post(url = self.url, headers = headers, json = params, timeout = None)  
        elif requestType == 'DELETE':
            self.result = requests.delete(url = self.url, headers = headers, json = params, timeout = None)
        elif requestType == 'PUT':
            self.result = requests.put(url = self.url, headers = headers, json = params, timeout = None)
            
        self.result = self.result.json()
        
        return json.dumps(self.result, indent=2)

    def headersCreator(self):
        self.stamp = str(int(time.time())*1000)
        self.data = '{}{}'.format(self.apiKey, self.stamp).encode('utf-8')
        self.signature = hmac.new(self.apiSecret, self.data, hashlib.sha256).digest()
        self.signature = base64.b64encode(self.signature)
        self.headers = {'X-PCK': self.apiKey, 'X-Stamp': self.stamp, 'X-Signature': self.signature, 'Content-Type' : 'application/json'}

        return self.headers

    def ticker(self, pairSymbol='', currency='', timeout=None):
        '''
        If pairSymbol is not set, ticker for all pairs will be returned in a json array.

        GET ../api/v2/ticker

        OR

        GET .../api/v2/ticker?pairSymbol=BTC_TRY

        OR

        GET .../api/v2/ticker/currency?symbol=USDT

        Parameters
        ----------

        pairSymbol\n
        currency

        Result
        ----------

        pair: Requested pair symbol\n
        pairNormalized: Requested pair symbol with '_' in between.\n
        timestamp: Current Unix time in milliseconds\n
        last: Last price\n
        high: Highest trade price in last 24 hours\n
        low: Lowest trade price in last 24 hours\n
        bid: Highest current bid\n
        ask: Lowest current ask\n
        open: Price of the opening trade in last 24 hours\n
        volume: Total volume in last 24 hours\n
        average: Average Price in last 24 hours\n
        daily: Price change in last 24 hours\n
        dailyPercent: Price change percent in last 24 hours\n
        denominatorSymbol: Denominator currency symbol of the pair\n
        numeratorSymbol: Numerator currency symbol of the pair\n
        '''

        self.urlMethod = '/api/v2/ticker'

        if pairSymbol:
            self.urlMethod += '?pairSymbol=' + pairSymbol
        elif currency:
            self.urlMethod += '/currency?symbol=' + currency

        return self.requestData(timeout=timeout)

    def trades(self, pairSymbol, last=''):
        '''
        GET .../api/v2/trades?pairSymbol=BTC_TRY

        OR

        GET .../api/v2/trades?pairSymbol=BTC_TRY&last=COUNT (Max. value for count parameter is 50)

        Parameters
        ----------

        (m)pairSymbol\n
        last (Max. value for last parameter is 50)

        Result
        ----------

        pair: Requested pair symbol\n
        pairNormalized: Request Pair symbol with '_' in between.\n
        numerator: Numerator currency for the requested pair\n
        denominator: Denominator currency for the requested pair\n
        date: Unix time of the trade in milliseconds\n
        tid: Trade ID\n
        price: Price of the trade\n
        amount: Amount of the trade\n
        '''

        if last and int(last)>50:
            last = '50'

        params = {'pairSymbol':pairSymbol, 'last':last}

        self.urlMethod = '/api/v2/trades?' + urlencode(params, True)

        return self.requestData()

    def orderBook(self, pairSymbol, limit=''):
        '''
        GET .../api/v2/orderbook?pairSymbol=BTC_TRY

        OR

        GET .../api/v2/orderbook?pairSymbol=BTC_TRY&limit=100

        Parameters
        -------------

        (m)pairSymbol\n
        limit

        Result
        --------------

        pairSymbol: string Mandatory\n
        limit: int Optional (default 100 max 1000)\n
        timestamp: Current Unix time in milliseconds\n
        bids: Array of current open bids on the orderbook.\n
        asks: Array of current open askss on the orderbook.\n
        '''

        if limit and int(limit)>1000:
            limit = '1000'

        params = {'pairSymbol':pairSymbol, 'limit':limit}

        self.urlMethod = '/api/v2/orderbook?' + urlencode(params, True)

        return self.requestData()

    def ohclData(self, pair, fromTimestamp='', toTimestamp=''):
        '''
        GET https://graph-api.btcturk.com/v1/ohlcs?pair=BTC_TRY

        OR

        GET https://graph-api.btcturk.com/v1/ohlcs?pair=BTC_TRY&from=1582132083&to=1582532083

        Parameters
        ---------------

        (m)pair\n
        from\n
        to\n

        Result
        ---------------

        pair: Requested pair symbol\n
        timestamp: Unix time in seconds\n
        open: Price of the opening trade on the time\n
        high: Highest trade price on the time\n
        low: Lowest trade price on the time\n
        close: Price of the closing trade on the time\n
        volume: Total volume on the time\n
        average: Average price on the time\n
        total: Total order amount on the time\n
        dailyChangeAmount: Amount of difference between Close and Open on the Date\n
        dailyChangePercentage: Percentage of difference between Close and Open on the Date\n
        '''

        params = {'pair':pair, 'from':fromTimestamp, 'to':toTimestamp}

        self.url = 'https://graph-api.btcturk.com/v1/ohlcs?' + urlencode(params, True)

        return self.requestData(createURL = False)

    def accountBalance(self):
        '''
        GET .../api/v1/users/balances\n

        Result
        -------------

        asset: Asset symbol\n
        assetname: Asset name\n
        balance: Total asset balance including open orders and pending withdrawal requests\n
        locked: Asset locked amount in open orders and withdrawal requests\n
        free: Asset available amount for trading\n
        '''

        self.urlMethod = '/api/v1/users/balances'

        return self.requestData(headers = self.headersCreator())

    def allOrders(self, pairSymbol, orderID='', startTime='', endTime='', page='', limit=''):
        '''
        GET .../api/v1/allOrders?pairSymbol=BTC_TRY

        Parameters
        --------------

        orderId: integer optional, If orderId set, it will return all orders greater than or equals to this order id\n
        (m)pairSymbol: pair symbol\n
        startTime: integer optional, start time\n
        endTime: integer optional, end time\n
        page: integer optional, page number\n
        limit: integer optional, default 100 max 1000\n

        Result
        -------------

        id: Order id\n
        price: Price of the order\n
        amount: Amount of the order\n
        quantity: quantity of the order\n
        pairsymbol: Pair of the order\n
        pairSymbolNormalized: Pair of the order with '_' in between.\n
        type: Type of order. Buy or Sell\n
        method: Method of order.\n
        orderClientId: Order client id created with (GUID if not set by user)\n
        time: Unix time the order was inserted at\n
        updateTime: Unix time last updated\n
        status: Status of the order. Untouched, Matched partialy, Canceled\n
        '''

        if limit and int(limit)>1000:
            limit = '1000'

        params = {'orderId':orderID, 'pairSymbol':pairSymbol, 'startTime':startTime, 'endTime':endTime, 'page':page, 'limit':limit}
    
        self.urlMethod = '/api/v1/allOrders?' + urlencode(params, True)

        return self.requestData(headers = self.headersCreator())
    
    def cancelOrder(self, orderID):
        '''
        DELETE .../api/v1/order?id=1

        Parameters
        -------------

        (m)orderID

        Result
        -------------
        
        Success true if the order cancellation succeeded. False if it failed.
        '''

        self.urlMethod = '/api/v1/order?id=' + orderID

        return self.requestData(requestType = 'DELETE', headers = self.headersCreator())

    def openOrders(self, pairSymbol=''):
        '''
        GET .../api/v1/openOrders?pairSymbol=BTC_TRY

        Parameters
        ---------------

        pairSymbol

        Result
        ---------------

        id: Order id\n
        price: Price of the order\n
        amount: Amount of the order\n
        quantity: quantity of the order\n
        stopPrice: stop order price if method is stop limit\n
        pairsymbol: Pair of the order\n
        pairSymbolNormalized: Pair of the order with '_' in between.\n
        type: Type of order. Buy or Sell\n
        method: Method of order. Limit, Stop Limit\n
        orderClientId: Order client id created with (GUID if not set by user)\n
        time: Unix time the order was inserted at\n
        updateTime: Unix time last updated\n
        status: Status of the order. Untouched (not matched), Partial (matched partially)\n
        leftAmount: Order left amount if it matched partialy\n
        '''
        
        self.urlMethod = '/api/v1/openOrders?pairSymbol=' + pairSymbol

        return self.requestData(headers = self.headersCreator())

    def submitOrder(self, quantity, price, orderMethod, orderType, pairSymbol, stopPrice='', newOrderClientId=''):
        '''
        POST .../api/v1/order

        Parameters
        -------------

        (m)quantity: 'decimal', Mandatory for market or limit orders.\n
        (m)price: 'decimal', Price field will be ignored for market orders. Market orders get filled with different prices until your order is completely filled. There is a 5% limit on the difference between the first price and the last price. İ.e. you can't buy at a price more than 5% higher than the best sell at the time of order submission and you can't sell at a price less than 5% lower than the best buy at the time of order submission.\n
        (m)stopPrice: 'decimal', For stop orders\n
        (m)newOrderClientId: 'string', GUID if user did not set.\n
        (m)orderMethod: 'enum', 'limit', 'market' or 'stoplimit'\n
        (m)orderType: 'enum', 'buy', 'sell'\n
        (m)pairSymbol: 'string', ex: 'BTCTRY', 'ETHTRY'\n

        Result
        -------------

        The result is a JSON object containing your order details and order ID if the request succeeded.

        Expected Errors
        ------------

        PARAMETERS_ERROR: One of the giving parameters is not correct.\n
        BALANCE_NOT_ENOUGH_WITHOUT_OPEN_ORDERS: You do not have enough funds for this operation.\n
        BALANCE_NOT_ENOUGH: The available funds is not enough for this operation.\n
        MIN_TOTAL: The order quantity is less than the minimum required.\n
        STOP_PRICE_GREATER_THAN_MARKET: Stop buy price must be above current price.\n
        STOP_PRICE_LESS_THAN_MARKET: Stop sell price must be bellow current price.\n
        '''

        params = {'quantity':quantity, 'price':price, 'stopPrice':stopPrice, 'newOrderClientId':newOrderClientId, 'orderMethod':orderMethod, 'orderType':orderType, 'pairSymbol':pairSymbol}

        self.urlMethod = '/api/v1/order'       
  
        return self.requestData(requestType = 'POST', headers = self.headersCreator(), params = params)

    def userTransactionsCrypto(self, tType='', symbol='', startDate='', endDate=''):
        '''
        POST .../api/v1/users/transactions/crypto

        Parameters
        --------------

        type: string array , {'deposit', 'withdrawal'}\n
        symbol: string array , {'btc', 'eth', 'xrp, ...etc.}\n
        startDate: long Optional timestamp if null will return last 30 days\n
        endDate: long Optional timestamp if null will return last 30 days\n
        '''

        params= {'type':tType, 'symbol':symbol, 'startDate':startDate, 'endDate':endDate}

        self.urlMethod = '/api/v1/users/transactions/crypto?' + urlencode(params, True)

        return self.requestData(headers = self.headersCreator())

    def userTransactionsFiat(self, balanceTypes='', currencySymbols='', startDate='', endDate=''):
        '''
        POST .../api/v1/users/transactions/fiat

        Parameters
        --------------

        balanceTypes: string array, {'deposit', 'withdrawal'}\n
        currencySymbols: string array, {'try' ...etc.}\n
        startDate: long Optional timestamp if null will return last 30 days\n
        endDate: long Optional timestamp if null will return last 30 days\n

        Result
        ---------------

        balanceType: Type of transaction (deposit, withdrawal)\n
        currencySymbol: Transaction currency symbol\n
        id: Transaction id\n
        timestamp: Unix timestamp\n
        amount: Transaction Amount\n
        fee: Transaction fee\n
        tax: Transaction tax\n
        '''

        params= {'balanceTypes':balanceTypes, 'currencySymbols':currencySymbols, 'startDate':startDate, 'endDate':endDate}

        self.urlMethod = '/api/v1/users/transactions/fiat' + urlencode(params, True)

        return self.requestData(headers = self.headersCreator())

    def userTransactionsTrade(self, tType='', symbol='', startDate='', endDate=''):
        '''
        GET .../api/v1/users/transactions/trade?type=buy&type=sell&symbol=btc&symbol=try&symbol=usdt

        Parameters
        --------------

        type: string array, {'buy', 'sell'}\n
        symbol: string array, {'btc', 'try', ...etc.}\n
        startDate: long Optional timestamp if null will return last 30 days\n
        endDate: long Optional timestamp if null will return last 30 days\n

        Result
        --------------

        price: Trade price\n
        numeratorSymbol: Trade pair numerator symbol\n
        denominatorSymbol: Trade pair denominator symbol\n
        orderType: Trade type (buy,sell)\n
        id: Trade id\n
        orderId: Order id which traded\n
        timestamp: Unix timestamp\n
        amount: Trade Amount (always negative if order type is sell)\n
        fee: Trade fee\n
        tax: Trade tax\n
        '''

        params= {'type':tType, 'symbol':symbol, 'startDate':startDate, 'endDate':endDate}

        self.urlMethod = '/api/v1/users/transactions/trade?' + urlencode(params, True)

        return self.requestData(headers = self.headersCreator())