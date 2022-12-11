# ibkr_tws_python

This script downloads the VIX futures (/VX) through Interactive Brokers API. 

Requirements:
- IBKR account + market data subscription for CFE 
- Python + ib_sync module + pandas module

Don't forget to allow IBKR API at Settings/API/Settings (Enable ActiveX and Sockets) and check if the socket port is correct (7497)