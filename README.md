# VIX Futures Price Fetcher

This project fetches the latest VIX index price and VIX futures prices for the next 8 months using the Interactive Brokers API. It includes functions to calculate VIX futures expiration dates and obtain the latest VIX and VIX futures prices.

## Prerequisites

1. An Interactive Brokers account with market data subscriptions for VIX and VIX futures (market data subscription for CFE) 
2. Trader Workstation (TWS) or IB Gateway running and connected to your Interactive Brokers account.
3. Python 3.x installed on your machine.
4. Required Python packages: `ib_insync`, `pandas`, `matplotlib`, `dateutil`.

To install the required Python packages, run the following command:

```bash
pip install ib_insync pandas matplotlib python-dateutil
```
## Usage

1. Import the `get_vix_and_vix_futures_prices()` function from the main script:

```python
from vix_index import get_vix_and_vix_futures_prices
```

Call the get_vix_and_vix_futures_prices() function to fetch the latest VIX index price and VIX futures prices:
```python
vix_data_list = get_vix_and_vix_futures_prices()
print(vix_data_list)
```



# ibkr_tws_python

This script downloads the VIX index and the VIX futures data through Interactive Brokers API and draws a chart.

Requirements:
- IBKR account + market data subscription for CFE 
- Python + ib_sync module + pandas module

Don't forget to allow IBKR API at Settings/API/Settings (Enable ActiveX and Sockets) and check if the socket port is correct (7497)