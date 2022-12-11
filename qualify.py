from ib_insync import *

# Create an IB object and connect to TWS or Gateway
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

# Define a list of expiry dates for the next 12 months
expiry_dates = ['202301', '202302', '202303', '202304', '202305', '202306',
                '202307', '202308']

# Loop over the expiry dates and add them to the contract
for expiry_date in expiry_dates:
    fut_contract = Contract()
    fut_contract.secType = 'FUT'
    fut_contract.exchange = 'CFE'
    fut_contract.currency = 'USD'
    fut_contract.symbol = 'VIX'
    fut_contract.tradingClass = 'VX'
    fut_contract.lastTradeDateOrContractMonth = expiry_date
    ib.qualifyContracts(fut_contract)
    print(expiry_date, fut_contract)
    ## Request real-time market data for the contract
    # ib.reqMktData(fut_contract, '', False, False)
    ## Print the last price for the contract
    # print(expiry_date, ib.ticker(fut_contract).last)
   
    # Request historical data for the contract
    data = ib.reqHistoricalData(
        fut_contract,
        endDateTime='',
        durationStr='1 D',
        barSizeSetting='1 day',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1
    )

    print(expiry_date, data)


