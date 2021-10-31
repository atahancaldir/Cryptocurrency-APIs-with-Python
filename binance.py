import time, base64, hmac, hashlib, requests, json
from urllib.parse import urlencode

class Binance:
    def __init__(self, apiKey, apiSecret):
        self.urlBase = 'https://api.binance.com'
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        
    def requestData(self, createURL = True, requestType = 'GET', data = {}, timeout = None):
        headers = {'X-MBX-APIKEY':self.apiKey, 'Content-Type':'application/json'}
        
        if createURL:
            self.url = self.urlBase + self.urlMethod

        if requestType == 'GET':
        	self.result = requests.get(url = self.url, headers = headers, data = data, timeout = timeout)
        elif requestType == 'POST':
        	self.result = requests.post(url = self.url, headers = headers, data = data , timeout = timeout)
        elif requestType == 'DELETE':
        	self.result = requests.delete(url = self.url, headers = headers, data = data, timeout = timeout)
        elif requestType == 'PUT':
        	self.result = requests.put(url = self.url, headers = headers, data = data, timeout = timeout)
        	
        self.result = self.result.json()
        
        return json.dumps(self.result, indent=2)
    
    def createSignature(self, data=''):
        if data:
            data += '&'
        data += 'timestamp=' + str(int(time.time())*1000)
        self.signature = hmac.new(self.apiSecret.encode('utf-8'), data.encode('utf-8'), hashlib.sha256).hexdigest()
        data += '&signature=' + self.signature

        return data

    def orderBook(self, symbol, limit=100):
        '''
        Parameters
        --------------
        (m)symbol(str): BTCTRY\n
        limit(int): Default 100; max 5000. Valid limits:[5, 10, 20, 50, 100, 500, 1000, 5000]\n
        
        Result
        ---------------
        {\n
            "lastUpdateId": 1027024,
            "bids": [
                [
                "4.00000000",     // PRICE
                "431.00000000"    // QTY
                ]
            ],
            "asks": [
                [
                "4.00000200",
                "12.00000000"
                ]
            ]
        }
        '''

        if limit and int(limit)>5000:
            limit = 5000

        params = {'symbol':symbol, 'limit':int(limit)}
        params = urlencode(params, True)

        self.urlMethod = '/api/v3/depth?' + params

        return self.requestData()

    def trades(self, symbol, limit=500):
        '''
        Get recent trades.

        Parameters
        -------------
        (m)symbol(str): BTCTRY\n
        limit(int): Default 500; max 1000

        Result
        --------------
        [
            {\n
                "id": 28457,
                "price": "4.00000100",
                "qty": "12.00000000",
                "quoteQty": "48.000012",
                "time": 1499865549590,
                "isBuyerMaker": true,
                "isBestMatch": true
            }
        ]
        '''

        if limit and int(limit)>1000:
            limit = 1000

        params = {'symbol':symbol, 'limit':int(limit)}
        params = urlencode(params, True)

        self.urlMethod = '/api/v3/trades?' + params

        return self.requestData()


    def historicalTrades(self, symbol, limit=500, fromId=0):
        '''
        Get older trades.

        Parameters
        ------------
        (m)symbol(str): BTCTRY\n
        limit(int): Default 500; max 1000.\n
        fromId(int): TradeId to fetch from. Default gets most recent trades.\n

        Result
        --------------
        [
            {\n
                "id": 28457,
                "price": "4.00000100",
                "qty": "12.00000000",
                "quoteQty": "48.000012",
                "time": 1499865549590,
                "isBuyerMaker": true,
                "isBestMatch": true
            }
        ]
        '''

        if limit and int(limit)>1000:
            limit = 1000

        params = {'symbol':symbol, 'limit':int(limit)}
        
        if fromId:
            params['fromId'] = fromId

        params = urlencode(params, True)

        self.urlMethod = '/api/v3/historicalTrades?' + params

        return self.requestData()

    def aggregateTrades(self, symbol, fromId=0, startTime='', endTime='', limit=500):
        '''
        Get compressed, aggregate trades. Trades that fill at the time, from the same taker order, with the same price will have the quantity aggregated.\n
        If both startTime and endTime are sent, time between startTime and endTime must be less than 1 hour.\n
        If fromId, startTime, and endTime are not sent, the most recent aggregate trades will be returned.
        
        Parameters
        --------------------
        (m)symbol(str): BTCTRY\n
        fromId(int): TradeId to fetch from. Default gets most recent trades.\n
        startTime(int): Timestamp in ms to get aggregate trades from INCLUSIVE.\n
        endTime(int): Timestamp in ms to get aggregate trades until INCLUSIVE.\n
        limit(int): Default 500; max 1000.\n

        Result
        -----------------
        [
            {\n
                "a": 26129,         // Aggregate tradeId
                "p": "0.01633102",  // Price
                "q": "4.70443515",  // Quantity
                "f": 27781,         // First tradeId
                "l": 27781,         // Last tradeId
                "T": 1498793709153, // Timestamp
                "m": true,          // Was the buyer the maker?
                "M": true           // Was the trade the best price match?
            }
        ]
        '''

        if limit and int(limit)>1000:
            limit = 1000

        params = {'symbol':symbol, 'limit':int(limit)}

        if fromId:
            params['fromId'] = fromId
        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        
        params = urlencode(params, True)

        self.urlMethod = '/api/v3/aggTrades?' + params

        return self.requestData()

    def klines(self, symbol, interval, startTime='', endTime='', limit=500):
        '''
        Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.\n
        If startTime and endTime are not sent, the most recent klines are returned.

        Parameters
        -----------------
        (m)symbol(str): BTCTRY\n
        (m)interval(enum)\n
        startTime(int)\n
        endTime(int)\n
        limit(int): Default 500; max 1000.\n

        Result
        ------------------
        [
            [\n
                1499040000000,      // Open time
                "0.01634790",       // Open
                "0.80000000",       // High
                "0.01575800",       // Low
                "0.01577100",       // Close
                "148976.11427815",  // Volume
                1499644799999,      // Close time
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume
                "28.46694368",      // Taker buy quote asset volume
                "17928899.62484339" // Ignore.
            ]
        ]
        '''

        if limit and int(limit)>1000:
            limit = 1000

        params = {'symbol':symbol, 'limit':int(limit), 'interval':interval}

        if startTime:
            params['startTime'] = startTime
        if endTime:
            params['endTime'] = endTime
        
        params = urlencode(params, True)

        self.urlMethod = '/api/v3/klines?' + params

        return self.requestData()

    def avgPrice(self, symbol):
        '''
        Current average price of a symbol

        Parameters
        ------------
        (m)symbol(str): BTCTRY

        Result
        ------------
        {\n
            "mins": 5,
            "price": "9.35751834"
        }
        '''

        params = {'symbol': symbol}
        params = urlencode(params, True)

        self.urlMethod = '/api/v3/avgPrice?' + params
        
        return self.requestData()

    def ticker24(self, symbol=''):
        '''
        24 hour rolling window price change statistics. Careful when accessing this with no symbol.\n
        If the symbol is not sent, tickers for all symbols will be returned in an array.

        Parameters
        --------------
        symbol(str): BTCTRY

        Result
        -------------
        {\n
            "symbol": "BNBBTC",
            "priceChange": "-94.99999800",
            "priceChangePercent": "-95.960",
            "weightedAvgPrice": "0.29628482",
            "prevClosePrice": "0.10002000",
            "lastPrice": "4.00000200",
            "lastQty": "200.00000000",
            "bidPrice": "4.00000000",
            "askPrice": "4.00000200",
            "openPrice": "99.00000000",
            "highPrice": "100.00000000",
            "lowPrice": "0.10000000",
            "volume": "8913.30000000",
            "quoteVolume": "15.30000000",
            "openTime": 1499783499040,
            "closeTime": 1499869899040,
            "firstId": 28385,   // First tradeId
            "lastId": 28460,    // Last tradeId
            "count": 76         // Trade count
        }
        '''

        params = {}

        if symbol:
            params['symbol'] = symbol
        
        params = urlencode(params, True)

        self.urlMethod = '/api/v3/ticker/24hr?' + params
        
        return self.requestData()

    def symbolPriceTicker(self, symbol=''):
        '''
        Latest price for a symbol or symbols.\n
        If the symbol is not sent, prices for all symbols will be returned in an array.

        Parameters
        ------------
        symbol(str): BTCTRY

        Result
        ------------
        {\n
            "symbol": "LTCBTC",
            "price": "4.00000200"
        }
        '''

        params = {}

        if symbol:
            params['symbol'] = symbol
        
        params = urlencode(params, True)

        self.urlMethod = '/api/v3/ticker/price?' + params
        
        return self.requestData()

    def symbolOrderBookTicker(self, symbol='', timeout=None):
        '''
        Best price/qty on the order book for a symbol or symbols.\n
        If the symbol is not sent, bookTickers for all symbols will be returned in an array.

        Parameters
        --------------
        symbol(str): BTCTRY

        Result
        --------------
        {\n
            "symbol": "LTCBTC",
            "bidPrice": "4.00000000",
            "bidQty": "431.00000000",
            "askPrice": "4.00000200",
            "askQty": "9.00000000"
        }
        '''

        params = {}

        if symbol:
            params['symbol'] = symbol
        
        params = urlencode(params, True)

        self.urlMethod = '/api/v3/ticker/bookTicker?' + params
        
        return self.requestData(timeout=timeout)

    def newOrder(self, symbol, side, oType, timeInForce='', quantity='', quoteOrderQty='', price='',
    newClientOrderId='', stopPrice='', icebergQty='', newOrderRespType='', recvWindow=''):
        '''
        Send in a new order.

        Parameters
        -------------
        (m)symbol(str): 'BTCTRY', ...\n
        (m)side(enum): 'BUY', 'SELL'\n
        (m)type(enum): 'LIMIT', 'MARKET', ...\n
        timeInForce(enum)\n
        quantity(float)\n
        quoteOrderQty(float)\n
        price(float)\n
        newClientOderId(str): A unique id among open orders. Automatically generated if not sent. Orders with the same newClientOrderID can be accepted only when the previous one is filled, otherwise the order will be rejected.\n
        stopPrice(float): Used with STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.\n
        icebergQty(float): 	Used with LIMIT, STOP_LOSS_LIMIT, and TAKE_PROFIT_LIMIT to create an iceberg order.\n
        newOrderRespType(enum): Set the response JSON. ACK, RESULT, or FULL; MARKET and LIMIT order types default to FULL, all other orders default to ACK.\n
        recvWindow(int): The value cannot be greater than 60000


        Mandatory parameters based on order type
        -----------------------------------------
        LIMIT: timeInForce, quantity, price\n
        MARKET: quantity or quoteOrderQty\n
        STOP_LOSS: quantity, stopPrice\n
        STOP_LOSS_LIMIT: timeInForce, quantity, price, stopPrice\n
        TAKE_PROFIT: quantity, stopPrice\n
        TAKE_PROFIT_LIMIT: timeInForce, quantity, price, stopPrice\n
        LIMIT_MAKER: quantity, price

        Some order types
        ----------------
        -MARKET: MARKET orders using the quantity field specifies the amount of the base asset the user wants to buy or sell at the market price.\n
        E.g. MARKET order on BTCUSDT will specify how much BTC the user is buying or selling.\n
        MARKET orders using quoteOrderQty specifies the amount the user wants to spend (when buying) or receive (when selling) the quote asset; the correct quantity will be determined based on the market liquidity and quoteOrderQty.\n
        E.g. Using the symbol BTCUSDT:\n
        BUY side, the order will buy as many BTC as quoteOrderQty USDT can.\n
        SELL side, the order will sell as much BTC needed to receive quoteOrderQty USDT.\n
        \n
        -STOP_LOSS: This will execute a MARKET order when the stopPrice is reached.\n
        \n
        -TAKE_PROFIT: This will execute a MARKET order when the stopPrice is reached.\n
        \n
        -LIMIT_MAKER: This is a LIMIT order that will be rejected if the order immediately matches and trades as a taker. This is also known as a POST-ONLY order.
        
        Additional Info
        ------------------
        -Any LIMIT or LIMIT_MAKER type order can be made an iceberg order by sending an icebergQty.\n
        -Any order with an icebergQty MUST have timeInForce set to GTC.\n
        -MARKET orders using quoteOrderQty will not break LOT_SIZE filter rules; the order will execute a quantity that will have the notional value as close as possible to quoteOrderQty. Trigger order price rules against market price for both MARKET and LIMIT versions:\n
        -Price above market price: STOP_LOSS BUY, TAKE_PROFIT SELL\n
        -Price below market price: STOP_LOSS SELL, TAKE_PROFIT BUY
        '''

        if recvWindow and int(recvWindow)>60000:
            recvWindow = 60000

        data = {'symbol':symbol, 'side':side, 'type':oType}

        if timeInForce:
            data['timeInForce'] = timeInForce
        if quantity:
            data['quantity'] = quantity
        if quoteOrderQty:
            data['quoteOrderQty'] = quoteOrderQty
        if price:
            data['price'] = price
        if newClientOrderId:
            data['newClientOrderId'] = newClientOrderId
        if stopPrice:
            data['stopPrice'] = stopPrice
        if icebergQty:
            data['icebergQty'] = icebergQty
        if newOrderRespType:
            data['newOrderRespType'] = newOrderRespType
        if recvWindow:
            data['recvWindow'] = recvWindow

        data = urlencode(data, True)
        data = self.createSignature(data)

        self.urlMethod = '/api/v3/order'

        return self.requestData(requestType='POST', data=data)

    def queryOrder(self, symbol, orderId='', origClientOrderId='', recvWindow=''):
        '''
        Check an order's status.

        Parameters
        -----------------
        (m)symbol(str): BTCTRY\n
        orderId(int)\n
        origClientOrderId(str)\n
        recvWindow(int): The value cannot be greater than 60000\n
        \n
        -Either orderId or origClientOrderId must be sent.\n
        -For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.

        Result
        -------------
        {\n
            "symbol": "LTCBTC",
            "orderId": 1,
            "orderListId": -1 //Unless part of an OCO, the value will always be -1.
            "clientOrderId": "myOrder1",
            "price": "0.1",
            "origQty": "1.0",
            "executedQty": "0.0",
            "cummulativeQuoteQty": "0.0",
            "status": "NEW",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY",
            "stopPrice": "0.0",
            "icebergQty": "0.0",
            "time": 1499827319559,
            "updateTime": 1499827319559,
            "isWorking": true,
            "origQuoteOrderQty": "0.000000"
        }
        '''

        if recvWindow and int(recvWindow)>60000:
            recvWindow = 60000

        data = {'symbol':symbol}

        if orderId:
            data['orderId'] = orderId
        if origClientOrderId:
            data['origClientOrderId'] = origClientOrderId
        if recvWindow:
            data['recvWindow'] = recvWindow

        data = urlencode(data, True)
        data = self.createSignature(data)

        self.urlMethod = '/api/v3/order'

        return self.requestData(data=data)

    def cancelOrder(self, symbol, orderId='', origClientOrderId='', newClientOrderId='', recvWindow=''):
        '''
        Cancel an active order.

        Parameters
        -----------------
        (m)symbol(str): BTCTRY\n
        orderId(int)\n
        origClientOrderId(str)\n
        newClientOrderId(str)\n
        recvWindow(int): The value cannot be greater than 60000\n
        \n
        -Either orderId or origClientOrderId must be sent.

        Result
        -------------
        {
            "symbol": "LTCBTC",
            "origClientOrderId": "myOrder1",
            "orderId": 4,
            "orderListId": -1, //Unless part of an OCO, the value will always be -1.
            "clientOrderId": "cancelMyOrder1",
            "price": "2.00000000",
            "origQty": "1.00000000",
            "executedQty": "0.00000000",
            "cummulativeQuoteQty": "0.00000000",
            "status": "CANCELED",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY"
        }
        '''

        if recvWindow and int(recvWindow)>60000:
            recvWindow = 60000

        data = {'symbol':symbol}

        if orderId:
            data['orderId'] = orderId
        if origClientOrderId:
            data['origClientOrderId'] = origClientOrderId
        if newClientOrderId:
            data['newClientOrderId'] = newClientOrderId
        if recvWindow:
            data['recvWindow'] = recvWindow

        data = urlencode(data, True)
        data = self.createSignature(data)

        self.urlMethod = '/api/v3/order'

        return self.requestData(requestType='DELETE', data=data)

    def cancelAllOrdersOfSymbol(self, symbol, recvWindow=''):
        '''
        Cancels all active orders on a symbol. This includes OCO orders.

        Parameters
        --------------
        (m)symbol(str): BTCTRY\n
        recvWindow(int): The value cannot be greater than 60000
        '''

        if recvWindow and int(recvWindow)>60000:
            recvWindow = 60000

        data = {'symbol':symbol}

        if recvWindow:
            data['recvWindow'] = recvWindow

        data = urlencode(data, True)
        data = self.createSignature(data)

        self.urlMethod = '/api/v3/openOrders'

        return self.requestData(requestType='DELETE', data=data)

    def openOrders(self, symbol='', recvWindow=''):
        '''
        Get all open orders on a symbol. Careful when accessing this with no symbol.

        Parameters
        -------------
        symbol: BTCTRY\n
        recvWindow: The value cannot be greater than 60000\n
        \n
        If the symbol is not sent, orders for all symbols will be returned in an array.

        Result
        ------------
        [\n
            {
                "symbol": "LTCBTC",
                "orderId": 1,
                "orderListId": -1, //Unless OCO, the value will always be -1
                "clientOrderId": "myOrder1",
                "price": "0.1",
                "origQty": "1.0",
                "executedQty": "0.0",
                "cummulativeQuoteQty": "0.0",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY",
                "stopPrice": "0.0",
                "icebergQty": "0.0",
                "time": 1499827319559,
                "updateTime": 1499827319559,
                "isWorking": true,
                "origQuoteOrderQty": "0.000000"
            }
        ]
        '''

        if recvWindow and int(recvWindow)>60000:
            recvWindow = 60000

        data = {}

        if symbol:
            data['symbol'] = symbol
        if recvWindow:
            data['recvWindow'] = recvWindow

        data = urlencode(data, True)
        data = self.createSignature(data)

        self.urlMethod = '/api/v3/openOrders'

        return self.requestData(data=data)

    def allOrders(self, symbol, orderId='', startTime='', endTime='', limit=500, recvWindow=''):
        '''
        Get all account orders; active, canceled, or filled.

        Parameters
        -------------
        (m)symbol(str): BTCTRY\n
        orderId(int)\n
        startTime(int)\n
        endTime(int)\n
        limit(int): Default 500; max 1000.\n
        recvWindow(int): The value cannot be greater than 60000\n
        \n
        -If orderId is set, it will get orders >= that orderId. Otherwise most recent orders are returned.\n
        -For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.

        Result
        ---------------
        [\n
            {
                "symbol": "LTCBTC",
                "orderId": 1,
                "orderListId": -1, //Unless OCO, the value will always be -1
                "clientOrderId": "myOrder1",
                "price": "0.1",
                "origQty": "1.0",
                "executedQty": "0.0",
                "cummulativeQuoteQty": "0.0",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY",
                "stopPrice": "0.0",
                "icebergQty": "0.0",
                "time": 1499827319559,
                "updateTime": 1499827319559,
                "isWorking": true,
                "origQuoteOrderQty": "0.000000"
            }
        ]
        '''

        if int(limit)>1000:
            limit = 1000

        if recvWindow and int(recvWindow)>60000:
            recvWindow = 60000

        data = {'symbol':symbol}

        if orderId:
            data['orderId'] = orderId
        if startTime:
            data['startTime'] = startTime
        if endTime:
            data['endTime'] = endTime
        if recvWindow:
            data['recvWindow'] = recvWindow

        data = urlencode(data, True)
        data = self.createSignature(data)

        self.urlMethod = '/api/v3/allOrders'

        return self.requestData(data=data)

    def newOCO(self, symbol, side, quantity, price, stopPrice, listClientOrderId='',
limitClientOrderId='', limitIcebergQty='', stopClientOrderId='', stopLimitPrice='',
stopIcerbergQty='', stopLimitTimeInForce='', newOrderRespType='', recvWindow=''):
        '''
        Send in a new OCO

        Parameters
        ---------------
        (m)symbol(str): BTCTRY\n
        (m)side(enum)\n
        (m)quantity(float)\n
        (m)price(float)\n
        (m)stopPrice(float)\n
        listClientOrderId(str): A unique Id for the entire orderList\n
        limitClientOrderId(str): A unique Id for the limit order\n
        limitIcebergQty(float): Used to make the LIMIT_MAKER leg an iceberg order.\n
        stopClientOrderId(str): A unique Id for the stop loss/stop loss limit leg\n
        stopLimitPrice(float): If provided, stopLimitTimeInForce is required.\n
        stopIcebergQty(float): Used with STOP_LOSS_LIMIT leg to make an iceberg order.\n
        stopLimitTimeInForce(enum): Valid values are GTC/FOK/IOC\n
        newOrderRespType(enum): Set the response JSON.\n
        recvWindow(int): The value cannot be greater than 60000

        -Price Restrictions:\n
            SELL: Limit Price > Last Price > Stop Price\n
            BUY: Limit Price < Last Price < Stop Price\n
        \n
        -Quantity Restrictions:\n
            Both legs must have the same quantity.\n
            ICEBERG quantities however do not have to be the same\n
        \n
        -Order Rate Limit\n
            OCO counts as 2 orders against the order rate limit.
        '''

        if recvWindow and int(recvWindow)>60000:
            recvWindow = 60000

        data = {'symbol':symbol, 'side':side, 'quantity':quantity, 'price':price, 'stopPrice':stopPrice}

        if listClientOrderId:
            data['listClientOrderId'] = listClientOrderId
        if limitClientOrderId:
            data['limitClientOrderId'] = limitClientOrderId
        if limitIcebergQty:
            data['limitIcebergQty'] = limitIcebergQty
        if stopClientOrderId:
            data['stopClientOrderId'] = stopClientOrderId
        if stopLimitPrice:
            data['stopLimitPrice'] = stopLimitPrice
        if stopIcerbergQty:
            data['stopIcerbergQty'] = stopIcerbergQty
        if stopLimitTimeInForce:
            data['stopLimitTimeInForce'] = stopLimitTimeInForce
        if newOrderRespType:
            data['newOrderRespType'] = newOrderRespType
        if recvWindow:
            data['recvWindow'] = recvWindow

        data = urlencode(data, True)
        data = self.createSignature(data)

        self.urlMethod = '/api/v3/order/oco'

        return self.requestData(requestType='POST', data=data)

    def cancelOCO(self, symbol, orderListId='', listClientOrderId='', newClientOrderId='', recvWindow=''):
        '''
        Cancel an entire Order List

        Parameters
        ----------------
        (m)symbol(str): BTCTRY\n
        orderListId(int): Either orderListId or listClientOrderId must be provided\n
        listClientOrderId(str): Either orderListId or listClientOrderId must be provided\n
        newClientOrderId(str): 	Used to uniquely identify this cancel. Automatically generated by default\n
        recvWindow(int): The value cannot be greater than 60000\n
        \n
        *Canceling an individual leg will cancel the entire OCO*
        '''

        if recvWindow and int(recvWindow)>60000:
            recvWindow = 60000

        data = {'symbol':symbol}

        if orderListId:
            data['orderListId'] = orderListId
        if listClientOrderId:
            data['listClientOrderId'] = listClientOrderId
        if newClientOrderId:
            data['newClientOrderId'] = newClientOrderId
        if recvWindow:
            data['recvWindow'] = recvWindow

        data = urlencode(data, True)
        data = self.createSignature(data)

        self.urlMethod = '/api/v3/orderList'

        return self.requestData(requestType='DELETE', data=data)

 ##################################
    def accountInfo(self, recvWindow=''):
        '''
        Get current account information.

        Parameters
        --------------
        recvWindow(int): The value cannot be greater than 60000
        '''

        if recvWindow and int(recvWindow)>60000:
            recvWindow = 60000

        data = self.createSignature()

        self.urlMethod = '/api/v3/account?' + data

        return self.requestData()