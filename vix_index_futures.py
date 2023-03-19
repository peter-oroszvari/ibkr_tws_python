from ib_insync import *
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from dateutil import relativedelta, rrule

def get_vix_expiration(year, month):
    """
    Calculate the VIX futures expiration date for the given year and month.

    The VIX futures expiration date is determined as follows:
    1. Find the third Friday of the specified month.
    2. Subtract 30 days from the third Friday.
    3. Find the previous Wednesday, which is the VIX futures expiration date.

    Args:
        year (int): The year for which to calculate the VIX futures expiration date.
        month (int): The month for which to calculate the VIX futures expiration date.

    Returns:
        datetime.date: The VIX futures expiration date for the given year and month.
    """
    third_friday = datetime.date(year, month, 15) + relativedelta.relativedelta(weekday=rrule.FR(3))
    expiration_day = third_friday - relativedelta.relativedelta(days=30, weekday=rrule.WE(-1))
    return expiration_day

def get_vix_and_vix_futures_prices():
    """
    Fetches the latest VIX index price and VIX futures prices for the next 8 months using Interactive Brokers API.

    This function initializes an Interactive Brokers (IB) connection, requests historical data for the VIX index
    and VIX futures contracts, and returns the latest price for each contract in a list of dictionaries.

    Note: Ensure that the IB TWS or IB Gateway is running and connected before executing this function.

    Returns:
        list: A list of dictionaries containing the contract symbols and their latest prices.
              Example: [{"symbol": "VXH23", "price": 25.5}, {"symbol": "VXJ23", "price": 26.3}, ...]
    """
    ib = IB()
    # Initialize empty lists to store price data and contract information
    price_list = [] 
    contract_list = []

    # Create an IB object and connect to TWS or Gateway
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=1)

    # Define a contract object for the VIX index
    vix_index = Contract()
    vix_index.secType = 'IND'       # Index security type
    vix_index.symbol = 'VIX'        # VIX index symbol
    vix_index.currency = 'USD'      # Currency of the VIX index
    vix_index.exchange = 'CBOE'     # Chicago Board Options Exchange

    # Qualify the VIX index contract to ensure its validity

    qualified_vix_contract = ib.qualifyContracts(vix_index)
    # print(qualified_vix_contract)

    # Request historical data for the VIX index from Interactive Brokers
    data = ib.reqHistoricalData(
        vix_index,                  # VIX index contract object
        endDateTime='',             # Empty string means "latest data available"
        durationStr='1 D',          # Duration of the historical data (1 day)
        barSizeSetting='1 day',     # Bar size of the historical data (1 day)
        whatToShow='TRADES',        # Data type to request (trade data)
        useRTH=True,                # Use regular trading hours data only
        formatDate=1                # Format date as UNIX timestamp
    )
    # print(data)

    # Convert the data to a Pandas DataFrame
    data_df = pd.DataFrame(data)
    # Get the last row of data using the tail() method
    last_row = data_df.tail(1)

    # Access the close field from the last row to get the last price
    last_price_vix = last_row['close']
    # Convert the last price from a Pandas Series to a NumPy array
    last_price_vix_value = last_price_vix.values
    # Print the last price of the VIX index
    print('VIX Index: ',last_price_vix_value[0])


    today = datetime.date.today()

    # Calculate the current month's VIX futures expiration date
    current_vix_expiration = get_vix_expiration(today.year, today.month)

    # If the current month's VIX futures have already expired, use the next month as the starting point
    if today > current_vix_expiration:
        starting_month = today + relativedelta.relativedelta(months=1)
    else:
        starting_month = today

    # If the starting month's VIX futures haven't expired yet, use the current month as the starting point
    if starting_month.month == today.month:
        expiry_dates = [(starting_month + relativedelta.relativedelta(months=i)).strftime('%Y%m') for i in range(0, 8)]
    else:
        expiry_dates = [(starting_month + relativedelta.relativedelta(months=i)).strftime('%Y%m') for i in range(-1, 7)]

    print('VIX Futures contracts expirity dates: ',expiry_dates)

    # Loop over the expiry dates and create a VIX futures contract for each expiry date
    for expiry_date in expiry_dates:
        fut_contract = Contract()      
        
        # Set the contract details 
        fut_contract.secType = 'FUT'
        fut_contract.exchange = 'CFE'
        fut_contract.currency = 'USD'
        fut_contract.symbol = 'VIX'
        fut_contract.tradingClass = 'VX'
        fut_contract.lastTradeDateOrContractMonth = expiry_date
        # Qualify the contract to obtain its full details from IBKR
        ib.qualifyContracts(fut_contract)
        # print(expiry_date, fut_contract.localSymbol)
        # Append the local symbol of the qualified contract to the contract_list
        contract_list.append(fut_contract.localSymbol)

        ## Request real-time market data for the contract
        ib.reqMktData(fut_contract, '', False, False)
        # Print the last price for the contract
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
        # Convert the data to a Pandas DataFrame
        data_df = pd.DataFrame(data)
        # Get the last row of data using the tail() method
        last_row = data_df.tail(1)

        # Access the close field from the last row to get the last price
        last_price = last_row['close']
        last_price_value = last_price.values
        price_list.append(last_price_value[0])
        #print(last_price_value)

    #i=0

    #for list in contract_list:
    #    print(f'Contract Symbol: {contract_list[i]}, Price: {price_list[i]}')
    #    i = i + 1 
        
    vix_data_list = [{"symbol": contract_list[i], "price": price_list[i]} for i in range(len(contract_list))]

    return vix_data_list
    
''''
# Draw a chart, define x,y values
x = contract_list
y = price_list

# Create the line chart
plt.plot(x, y)
plt.axhline(y = last_price_vix_value, color ="red", linestyle ="--")
label = "VIX Index: {}".format(last_price_vix_value)
plt.legend([label])


# Add labels and title
plt.xlabel('Symbol')
plt.ylabel('Volatility')
plt.title('VIX Futures curve')

for i in range(len(x)):
    plt.text(x[i], y[i], y[i])

plt.show()
'''