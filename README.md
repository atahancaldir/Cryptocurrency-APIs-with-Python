#Cryptocurrency APIs with Python
This project includes a Python expression of some of the Cryptocurrency stock markets such as BtcTurk, Binance, etc.

New APIs will be included in the future

#Where to use these API features?
API features can be used for diverse aims such as automated trading algorithms, arbitrage, comparing cryptocurrency prices from different stock markets, etc.

#How to use APIs?
First, you need to create an API key with an API secret from the website of the stock market (DO NOT SHARE WITH ANYBODY ELSE!). Then, imlement them while creating the object from the relevant class. (e.g.: For BtcTurk, while creating an BtcTurk object from the btcTurk.py file, you have give the API key and API secret as parameters to let the code enter the BtcTurk system with your information).

#Is it safe to use the APIs?
Yes, these APIs are released by the stock markets themselves. You can reach the official API documents of some of the stock markets with the links below. The point which makes it safe is that everytime you try to make a transaction on the stock markets, a special algorithm creates a unique signature for you. The signature is special to your signature, date, time, and more according to the stock market. So, every transaction needs a new signature. Unless you give your API information somebody else, it is fully safe.

#Official API documents
BtcTurk: https://docs.btcturk.com
Binance: https://github.com/binance/binance-spot-api-docs
