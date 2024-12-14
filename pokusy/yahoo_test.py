from yahooquery import Ticker

symbols = ['fb', 'aapl', 'amzn', 'nflx', 'goog']

faang = Ticker(symbols)

allfin = faang.all_financial_data('q')
print(allfin)
calev = faang.calendar_events
det = calev['aapl']
print(det)

test = faang.earnings
print(test['aapl'])

"""
for array in allfin:
    for row in array:
        print(row)
"""