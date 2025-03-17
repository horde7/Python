import pandas as pd
import matplotlib.pyplot as plt
import requests
import time
from datetime import datetime
import json

def get_goog_tickers():
    """
    Get a list of tickers that contain 'GOOG'
    
    Returns:
    list: List of tickers containing 'GOOG'
    """
    # Hard-coded list of Google tickers
    goog_tickers = [
        {"symbol": "GOOG", "name": "Alphabet Inc. (Google) Class C"},
        {"symbol": "GOOGL", "name": "Alphabet Inc. (Google) Class A"}
    ]
    
    return goog_tickers

def get_api_key():
    """
    Get FMP API key from user
    
    Returns:
    str: API key
    """
    api_key = input("Enter your Financial Modeling Prep API key: ")
    return api_key

def get_quarterly_income_statement(ticker, api_key):
    """
    Get quarterly income statement data from FMP API
    
    Parameters:
    ticker (str): Stock ticker symbol
    api_key (str): FMP API key
    
    Returns:
    list: List of quarterly income statement data
    """
    url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period=quarter&apikey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching income statement: {response.status_code}")
        return []

def get_quarterly_balance_sheet(ticker, api_key):
    """
    Get quarterly balance sheet data from FMP API
    
    Parameters:
    ticker (str): Stock ticker symbol
    api_key (str): FMP API key
    
    Returns:
    list: List of quarterly balance sheet data
    """
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period=quarter&apikey={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error fetching balance sheet: {response.status_code}")
        return []

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

def find_closest_price(date_str, price_data):
    """
    Find the closest price to a given date
    
    Parameters:
    date_str (str): Date string in YYYY-MM-DD format
    price_data (list): List of price data dictionaries
    
    Returns:
    float: Closing price on the closest date
    """
    target_date = datetime.strptime(date_str, "%Y-%m-%d")
    closest_price = None
    min_diff = float('inf')
    
    for price_point in price_data:
        price_date = datetime.strptime(price_point['date'], "%Y-%m-%d")
        diff = abs((target_date - price_date).days)
        
        if diff < min_diff:
            min_diff = diff
            closest_price = price_point['close']
    
    return closest_price

def calculate_quarterly_pe(ticker, year, api_key):
    """
    Calculate quarterly P/E ratios for a given ticker and year
    
    Parameters:
    ticker (str): Stock ticker symbol
    year (int): Year to analyze
    api_key (str): FMP API key
    
    Returns:
    pd.DataFrame: DataFrame with quarterly P/E ratios
    """
    print(f"Fetching quarterly financial data for {ticker} in {year}...")
    
    # Get income statement data
    income_data = get_quarterly_income_statement(ticker, api_key)
    if not income_data:
        print("Failed to retrieve income statement data.")
        return pd.DataFrame()
    
    # Get balance sheet data
    balance_data = get_quarterly_balance_sheet(ticker, api_key)
    if not balance_data:
        print("Failed to retrieve balance sheet data.")
        return pd.DataFrame()
    
    # Filter data for the specified year
    income_data = [item for item in income_data if item['date'].startswith(str(year))]
    balance_data = [item for item in balance_data if item['date'].startswith(str(year))]
    
    if not income_data:
        print(f"No income statement data available for {ticker} in {year}")
        return pd.DataFrame()
    
    if not balance_data:
        print(f"No balance sheet data available for {ticker} in {year}")
        return pd.DataFrame()
    
    # Get historical price data for the year
    from_date = f"{year}-01-01"
    to_date = f"{year}-12-31"
    price_data = get_historical_price(ticker, from_date, to_date, api_key)
    
    if not price_data:
        print(f"No historical price data available for {ticker} in {year}")
        return pd.DataFrame()
    
    # Calculate P/E for each quarter
    results = []
    
    for quarter in income_data:
        try:
            quarter_date = quarter['date']
            quarter_month = int(quarter_date.split('-')[1])
            quarter_num = (quarter_month - 1) // 3 + 1
            
            # Get net income
            net_income = quarter['netIncome']
            
            # Find matching balance sheet data
            matching_balance = next((item for item in balance_data if item['date'] == quarter_date), None)
            if not matching_balance:
                print(f"No matching balance sheet data for {quarter_date}")
                continue
            
            # Get shares outstanding
            # FMP generally uses 'commonStock' for shares outstanding, but we'll check alternatives
            shares = matching_balance.get('commonStock')
            if not shares or shares == 0:
                shares = matching_balance.get('commonStockSharesOutstanding')
            
            if not shares or shares == 0:
                print(f"Could not find valid shares outstanding for {quarter_date}")
                continue
            
            # Calculate EPS
            eps = net_income / shares
            
            # Get stock price at quarter end
            price = find_closest_price(quarter_date, price_data)
            
            if not price:
                print(f"Could not find price data for {quarter_date}")
                continue
            
            # Calculate P/E ratio
            pe_ratio = price / eps if eps != 0 else float('inf')
            
            results.append({
                'Quarter': f"Q{quarter_num} {year}",
                'Date': quarter_date,
                'Price': price,
                'EPS': eps,
                'P/E Ratio': pe_ratio
            })
            
        except Exception as e:
            print(f"Error calculating P/E for {quarter_date}: {e}")
    
    # Sort results by date
    results.sort(key=lambda x: x['Date'])
    
    return pd.DataFrame(results)

def main():
    # Get list of Google tickers
    print("Getting list of Google tickers...")
    goog_tickers = get_goog_tickers()
    
    # Display available tickers
    print("\nAvailable Google tickers:")
    for i, ticker_info in enumerate(goog_tickers):
        print(f"{i+1}. {ticker_info['symbol']} - {ticker_info['name']}")
    
    # Let user select a ticker
    while True:
        try:
            selection = input("\nSelect a ticker number (or 0 to quit): ")
            selection = int(selection)
            if selection == 0:
                return
            if 1 <= selection <= len(goog_tickers):
                break
            print(f"Please enter a number between 1 and {len(goog_tickers)}")
        except ValueError:
            print("Please enter a valid number")
    
    selected_ticker = goog_tickers[selection-1]['symbol']
    
    # Get API key
    api_key = get_api_key()
    
    # Set the year
    year = 2010
    
    print(f"\nFetching quarterly P/E ratios for {selected_ticker} in {year}...")
    
    # Calculate quarterly P/E ratios
    quarterly_pe = calculate_quarterly_pe(selected_ticker, year, api_key)
    
    # Check if we have data before proceeding
    if quarterly_pe.empty:
        print("No P/E data available for the specified ticker and year.")
        return
    
    # Display results
    print("\nQuarterly P/E Ratios:")
    print(quarterly_pe)
    
    # Save to CSV
    csv_filename = f"{selected_ticker}_PE_Ratios_{year}.csv"
    quarterly_pe.to_csv(csv_filename, index=False)
    print(f"Data saved to {csv_filename}")
    
    # Plot the results
    plt.figure(figsize=(10, 6))
    quarters = quarterly_pe['Quarter'].tolist()
    pe_ratios = quarterly_pe['P/E Ratio'].tolist()
    
    plt.bar(range(len(quarters)), pe_ratios)
    plt.xticks(range(len(quarters)), quarters)
    plt.title(f"{selected_ticker} Quarterly P/E Ratios - {year}")
    plt.ylabel("P/E Ratio")
    plt.xlabel("Quarter")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Add values above bars
    for i, value in enumerate(pe_ratios):
        plt.text(i, value + 1, f"{value:.2f}", ha='center')
    
    plt.tight_layout()
    plt.savefig(f"{selected_ticker}_PE_Ratios_{year}.png")
    print(f"Plot saved as {selected_ticker}_PE_Ratios_{year}.png")
    plt.show()

if __name__ == "__main__":
    main()
