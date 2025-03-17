import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

def get_apple_earnings_since_2015():
    """
    Retrieve quarterly earnings data for Apple (AAPL) since 2015.
    
    Returns:
    pandas.DataFrame: Quarterly earnings data
    """
    # Create ticker object for Apple
    ticker = yf.Ticker("AAPL")
    
    # Get earnings data
    earnings = ticker.earnings_history
    
    if earnings is None or earnings.empty:
        print("No earnings data available for AAPL")
        return None
    
    # Filter for data since 2015
    earnings = earnings[earnings['Earnings Date'].dt.year >= 2015]
    
    # Format the data
    earnings = earnings.sort_values('Earnings Date')
    
    # Convert earnings date to readable format and create fiscal quarter notation
    earnings['Quarter'] = earnings['Earnings Date'].dt.strftime('%Y-Q%q')
    
    # Create fiscal year column
    # Apple's fiscal year ends in September
    def get_fiscal_year(date):
        if date.month >= 10:  # October onwards is next fiscal year
            return date.year + 1
        return date.year
    
    earnings['Fiscal Year'] = earnings['Earnings Date'].apply(get_fiscal_year)
    
    return earnings

def visualize_apple_earnings(earnings_data):
    """
    Create visualizations of Apple's quarterly earnings.
    
    Parameters:
    earnings_data (pandas.DataFrame): The quarterly earnings data
    """
    plt.figure(figsize=(15, 10))
    
    # EPS visualization
    plt.subplot(2, 1, 1)
    width = 0.35
    x = np.arange(len(earnings_data['Quarter']))
    
    plt.bar(x - width/2, earnings_data['EPS Actual'], width, label='EPS Actual')
    plt.bar(x + width/2, earnings_data['EPS Estimate'], width, label='EPS Estimate')
    
    plt.title('Apple (AAPL) Quarterly EPS Since 2015')
    plt.xlabel('Quarter')
    plt.ylabel('Earnings Per Share ($)')
    plt.xticks(x, earnings_data['Quarter'], rotation=90)
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Surprise percentage visualization
    plt.subplot(2, 1, 2)
    colors = ['green' if x >= 0 else 'red' for x in earnings_data['Surprise(%)']]
    plt.bar(earnings_data['Quarter'], earnings_data['Surprise(%)'], color=colors)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.title('Apple (AAPL) Earnings Surprise % Since 2015')
    plt.xlabel('Quarter')
    plt.ylabel('Surprise (%)')
    plt.xticks(rotation=90)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("AAPL_earnings_since_2015.png")
    plt.show()

def display_apple_earnings_since_2015():
    """
    Display and analyze Apple's quarterly earnings since 2015.
    """
    print("Retrieving Apple (AAPL) quarterly earnings data since 2015...\n")
    
    # Get earnings data
    earnings_data = get_apple_earnings_since_2015()
    
    if earnings_data is None:
        return
    
    # Display earnings data
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 1000)
    print("Quarterly Earnings for Apple (AAPL) since 2015:")
    display_df = earnings_data[['Earnings Date', 'Quarter', 'Fiscal Year', 'EPS Estimate', 'EPS Actual', 'Surprise(%)']]
    display_df = display_df.sort_values('Earnings Date', ascending=False)  # Show most recent first
    print(display_df)
    
    # Basic analysis
    beat_count = sum(earnings_data['EPS Actual'] > earnings_data['EPS Estimate'])
    miss_count = sum(earnings_data['EPS Actual'] < earnings_data['EPS Estimate'])
    match_count = sum(earnings_data['EPS Actual'] == earnings_data['EPS Estimate'])
    
    print(f"\nSummary for {len(earnings_data)} quarters since 2015:")
    print(f"Beat expectations: {beat_count} times ({beat_count/len(earnings_data)*100:.1f}%)")
    print(f"Missed expectations: {miss_count} times ({miss_count/len(earnings_data)*100:.1f}%)")
    print(f"Met expectations: {match_count} times ({match_count/len(earnings_data)*100:.1f}%)")
    print(f"Average surprise: {earnings_data['Surprise(%)'].mean():.2f}%")
    
    # Analysis by fiscal year
    print("\nPerformance by Fiscal Year:")
    yearly_analysis = earnings_data.groupby('Fiscal Year').agg(
        avg_eps_actual=('EPS Actual', 'mean'),
        avg_eps_estimate=('EPS Estimate', 'mean'),
        avg_surprise=('Surprise(%)', 'mean'),
        beat_count=('Surprise(%)', lambda x: sum(x > 0)),
        quarters=('Quarter', 'count')
    )
    print(yearly_analysis)
    
    # Create visualization
    visualize_apple_earnings(earnings_data.sort_values('Earnings Date'))

if __name__ == "__main__":
    display_apple_earnings_since_2015()