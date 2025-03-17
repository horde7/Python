from yahooquery import Ticker

def test_yahoo1():
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
def test_yahoo2():
    symbols = ['fb', 'aapl', 'amzn', 'nflx', 'goog']
    faang = Ticker(symbols)
    test = faang.earnings
    print(test['aapl'])

# test_yahoo1()
test_yahoo2()
    