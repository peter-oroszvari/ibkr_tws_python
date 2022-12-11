# ibkr_tws_python

This script downloads the VIX index and the VIX futures data through Interactive Brokers API and draws a chart.

Requirements:
- IBKR account + market data subscription for CFE 
- Python + ib_sync module + pandas module

Don't forget to allow IBKR API at Settings/API/Settings (Enable ActiveX and Sockets) and check if the socket port is correct (7497)