import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import argparse

    ticker = yf.Ticker("AAPL")
    
    # Get earnings data
    earnings = ticker.earnings_history
    
    if earnings is None or earnings.empty:
        print(f"No earnings data available for {ticker_symbol}")
        
    
    # Format the data
    earnings = earnings.sort_values('Earnings Date', ascending=False)
    earnings = earnings.head(periods)
    earnings = earnings.sort_values('Earnings Date')
    
    # Convert earnings date to readable format
    earnings['Quarter'] = earnings['Earnings Date'].dt.strftime('%Y-Q%q')