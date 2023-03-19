from ib_insync import *
import pandas as pd

# Connect to IBKR
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

vix= Index('VIX', 'CBOE')
ib.qualifyContracts(vix)

ib.reqMarketDataType(4)


#contracts = ib.reqContractDetails(Option(symbol='VIX'))
#df = util.df(contracts)
#print(df)
#df.to_csv(r'vix.csv', header=None, index=None, sep=' ', mode='a')

[ticker] = ib.reqTickers(vix)

vixValue = ticker.marketPrice()


chains = ib.reqSecDefOptParams(vix.symbol, '', vix.secType, vix.conId)

df = util.df(chains)
print(df)

chain = next(c for c in chains if c.tradingClass == 'VIX' and c.exchange == 'SMART')
print(chain)

print(chain.strikes)
strikes = chain.strikes
expirations = sorted(exp for exp in chain.expirations)[:3]
rights = ['P', 'C']

contracts = [Option('VIX', expiration, strike, right, 'SMART', tradingClass='VIX')
        for right in rights
        for expiration in expirations
        for strike in strikes]

contracts = ib.qualifyContracts(*contracts)
len(contracts)

tickers = ib.reqTickers(*contracts)
'''
i = 0 
for ticker in tickers:
    print(tickers[i].contract.lastTradeDateOrContractMonth)
    print(tickers[i].contract.symbol)
    print(tickers[i].contract.right)
    print(tickers[i].bidGreeks)
    print(tickers[i].askGreeks)

    i += 1 
    '''

