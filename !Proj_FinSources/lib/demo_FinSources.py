import lib_FInSources

# https://site.financialmodelingprep.com/developer/docs#earnings-historical-earnings
API_KEY = "RZ6QTubSErql5tnHU7wGy2jzyonyujsQ"
ticker = "AAPL"
yearFrom = 2010
yearTo = 2025
fromDate = f"{yearFrom}-01-01"
toDate = f"{yearTo}-12-31"


data = lib_FInSources.get_historical_price(ticker, fromDate, toDate, API_KEY)
print(data)