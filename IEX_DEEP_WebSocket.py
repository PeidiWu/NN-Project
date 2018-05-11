import pyEX.pyEX.marketdata.ws

x = pyEX.pyEX.marketdata.ws.deepWS('aapl', channels='deep', on_data=print)
x.run()