import time
from ib_insync import *
import matplotlib.pyplot as plt

volatility = []
contract_list = []

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)
vix_index = Contract()
vix_index.secType = 'IND'
vix_index.symbol = 'VIX'
vix_index.currency = 'USD'
vix_index.exchange = 'CBOE'

Ticker=ib.reqMktData(vix_index)
if True:
    ib.sleep(1)
    print(Ticker.last)
    vix_index_value = Ticker.last

# Define a list of expiry dates for the next 12 months
expiry_dates = ['202212','202301', '202302', '202303', '202304', '202305', '202306',
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
    print(expiry_date, fut_contract.localSymbol)
    contract_list.append(fut_contract.localSymbol)
    Ticker=ib.reqMktData(fut_contract)
    if True:
        ib.sleep(3)
        print(Ticker.last)
        volatility.append(Ticker.last)

    # Draw a chart, define x,y values
x = contract_list
y = volatility

# Create the line chart
plt.plot(x, y)
plt.axhline(y = vix_index_value, color ="red", linestyle ="--")
label = "VIX Index: {}".format(vix_index_value)
plt.legend([label])


# Add labels and title
plt.xlabel('Symbol')
plt.ylabel('Volatility')
plt.title('VIX Futures curve')

for i in range(len(x)):
    plt.text(x[i], y[i], y[i])

plt.show()
