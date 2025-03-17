import requests

def get_historical_price(ticker, from_date, to_date, api_key):
    """
    Get historical stock price data from FMP API
    
    Parameters:
    ticker (str): Stock ticker symbol
    from_date (str): Start date in YYYY-MM-DD format
    to_date (str): End date in YYYY-MM-DD format
    api_key (str): FMP API key
    
    Returns:
    list: List of historical price data
    """
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from={from_date}&to={to_date}&apikey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('historical', [])
    else:
        print(f"Error fetching historical prices: {response.status_code}")
        return []