import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

def get_quarterly_earnings(ticker_symbol, periods=8):
    """
    Retrieve quarterly earnings data for a specified stock ticker.
    
    Parameters:
    ticker_symbol (str): The stock ticker symbol
    periods (int): Number of recent quarters to display (default: 8)
    
    Returns:
    pandas.DataFrame: Quarterly earnings data
    """
    # Create ticker object
    ticker = yf.Ticker(ticker_symbol)
    
    # Get earnings data
    earnings = ticker.earnings_history
    
    if earnings is None or earnings.empty:
        print(f"No earnings data available for {ticker_symbol}")
        return None
    
    # Format the data
    earnings = earnings.sort_values('Earnings Date', ascending=False)
    earnings = earnings.head(periods)
    earnings = earnings.sort_values('Earnings Date')
    
    # Convert earnings date to readable format
    earnings['Quarter'] = earnings['Earnings Date'].dt.strftime('%Y-Q%q')
    
    return earnings

def visualize_earnings(earnings_data, ticker_symbol):
    """
    Create a visualization of quarterly earnings.
    
    Parameters:
    earnings_data (pandas.DataFrame): The quarterly earnings data
    ticker_symbol (str): The stock ticker symbol
    """
    plt.figure(figsize=(12, 6))
    
    # EPS visualization
    plt.subplot(1, 2, 1)
    plt.bar(earnings_data['Quarter'], earnings_data['EPS Actual'])
    plt.plot(earnings_data['Quarter'], earnings_data['EPS Estimate'], 'r--o', label='EPS Estimate')
    plt.title(f'{ticker_symbol} Quarterly EPS')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Surprise percentage visualization
    plt.subplot(1, 2, 2)
    plt.bar(earnings_data['Quarter'], earnings_data['Surprise(%)'])
    plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
    plt.title(f'{ticker_symbol} Earnings Surprise %')
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f"{ticker_symbol}_earnings.png")
    plt.show()

def display_earnings_info(ticker_symbol, periods=8):
    """
    Display quarterly earnings information for a stock.
    
    Parameters:
    ticker_symbol (str): The stock ticker symbol
    periods (int): Number of recent quarters to display
    """
    print(f"\nRetrieving quarterly earnings data for {ticker_symbol}...\n")
    
    # Get earnings data
    earnings_data = get_quarterly_earnings(ticker_symbol, periods)
    
    if earnings_data is None:
        return
    
    # Display earnings data
    pd.set_option('display.max_columns', None)
    print(f"Quarterly Earnings for {ticker_symbol}:")
    print(earnings_data[['Quarter', 'EPS Estimate', 'EPS Actual', 'Surprise(%)']])
    
    # Basic calculations
    beat_count = sum(earnings_data['EPS Actual'] > earnings_data['EPS Estimate'])
    miss_count = sum(earnings_data['EPS Actual'] < earnings_data['EPS Estimate'])
    match_count = sum(earnings_data['EPS Actual'] == earnings_data['EPS Estimate'])
    
    print(f"\nSummary for last {len(earnings_data)} quarters:")
    print(f"Beat expectations: {beat_count} times")
    print(f"Missed expectations: {miss_count} times")
    print(f"Met expectations: {match_count} times")
    print(f"Average surprise: {earnings_data['Surprise(%)'].mean():.2f}%")
    
    # Create visualization
    visualize_earnings(earnings_data, ticker_symbol)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Retrieve quarterly earnings data for a stock.')
    parser.add_argument('ticker', type=str, help='Stock ticker symbol (e.g., AAPL)')
    parser.add_argument('--periods', type=int, default=8, help='Number of recent quarters to display (default: 8)')
    
    args = parser.parse_args()
    display_earnings_info(args.ticker.upper(), args.periods)
