# Cryptocurrency APIs with Python 💸

**The development has been done in 2021-2022. Please DO NOT use the code without checking the updated API documentations! The responsibility of the consequences are on the user.**

This project includes a Python expression of some of the cryptocurrency exchange markets such as BtcTurk, Binance, etc.

### Where to use these API features?

API features can be used for diverse aims such as;

* Automated trading algorithms
* Arbitrage
* Comparing cryptocurrency prices of different cryptocurrency exchange markets
* Saving your data with advanced data science techniques

### How to use APIs?

First, you need to create an API key with an API secret from the website of the exchange market (**DO NOT SHARE YOUR KEY WITH ANYBODY ELSE!**). Then, imlement them into your code while creating the object from the relevant class.

### Is it safe to use the APIs?

Yes, these APIs are released by the cryptocurrency exchange markets themselves. You can reach the official API documents of some of the exchange markets with the links below. The point which makes it safe is that everytime you try to make a transaction on the exchange markets, a special algorithm creates a unique signature for you. The signature is special to your signature, date, time, and more according to the exchange market. Hence, every transaction needs a new signature. Unless you give your API information somebody else, it is fully safe.

# Usage

```python
from btcTurk.py import BtcTurk

btcturk = BtcTurk(your_API_key, your_API_secret)
result = btcturk.ticker('BTC_TRY') #It will return a JSON string

print(result)
```

There are lots of functions provided from exchange markets. You can check the functions with their explanations in the .py files.

# Official API documents

[BtcTurk](https://docs.btcturk.com) 
[Binance](https://github.com/binance/binance-spot-api-docs)

# Warning 📛

These files are designed to do **REAL** transactions. Please DO NOT use them unless you know what you're doing!
