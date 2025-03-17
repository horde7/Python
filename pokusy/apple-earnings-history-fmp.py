import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import os

# You'll need to get your own API key by signing up at https://financialmodelingprep.com/developer/docs/
# Free tier allows limited requests per day
API_KEY = "RZ6QTubSErql5tnHU7wGy2jzyonyujsQ"  # Replace with your actual API key

def get_apple_earnings_since_2015(api_key):
    """
    Retrieve quarterly earnings data for Apple (AAPL) since 2015 using Financial Modeling Prep API.
    
    Parameters:
    api_key (str): Your Financial Modeling Prep API key
    
    Returns:
    pandas.DataFrame: Quarterly earnings data
    """
    # Base URL for Financial Modeling Prep API
    base_url = "https://financialmodelingprep.com/api/v3/earnings-surprises/AAPL"
    
    # Make API request
    response = requests.get(f"{base_url}?apikey={api_key}")
    
    if response.status_code != 200:
        print(f"Error fetching data: Status code {response.status_code}")
        print(response.text)
        return None
    
    # Convert to DataFrame
    earnings_data = pd.DataFrame(response.json())
    
    # Filter for data since 2015
    earnings_data['date'] = pd.to_datetime(earnings_data['date'])
    earnings_data = earnings_data[earnings_data['date'].dt.year >= 2015]
    
    # Rename columns to match previous script
    earnings_data = earnings_data.rename(columns={
        'date': 'Earnings Date',
        'estimatedEPS': 'EPS Estimate',
        'actualEPS': 'EPS Actual',
        'surprisePercentage': 'Surprise(%)'
    })
    
    # Format the data
    earnings_data = earnings_data.sort_values('Earnings Date')
    
    # Add quarter notation
    earnings_data['Quarter'] = earnings_data['Earnings Date'].dt.strftime('%Y-Q%q')
    
    # Create fiscal year column (Apple's fiscal year ends in September)
    def get_fiscal_year(date):
        if date.month >= 10:  # October onwards is next fiscal year
            return date.year + 1
        return date.year
    
    earnings_data['Fiscal Year'] = earnings_data['Earnings Date'].apply(get_fiscal_year)
    
    return earnings_data

def get_apple_quarterly_revenue_since_2015(api_key):
    """
    Retrieve quarterly revenue data for Apple (AAPL) since 2015 using Financial Modeling Prep API.
    
    Parameters:
    api_key (str): Your Financial Modeling Prep API key
    
    Returns:
    pandas.DataFrame: Quarterly revenue data
    """
    # Base URL for Financial Modeling Prep API income statements
    base_url = "https://financialmodelingprep.com/api/v3/income-statement/AAPL"
    
    # Make API request for quarterly data
    response = requests.get(f"{base_url}?period=quarter&limit=100&apikey={api_key}")
    
    if response.status_code != 200:
        print(f"Error fetching revenue data: Status code {response.status_code}")
        print(response.text)
        return None
    
    # Convert to DataFrame
    revenue_data = pd.DataFrame(response.json())
    
    # Filter for data since 2015
    revenue_data['date'] = pd.to_datetime(revenue_data['date'])
    revenue_data = revenue_data[revenue_data['date'].dt.year >= 2015]
    
    # Select only relevant columns
    revenue_data = revenue_data[['date', 'revenue', 'netIncome']].copy()
    
    # Rename columns
    revenue_data = revenue_data.rename(columns={
        'date': 'Report Date',
        'revenue': 'Revenue',
        'netIncome': 'Net Income'
    })
    
    # Format the data
    revenue_data = revenue_data.sort_values('Report Date')
    revenue_data['Quarter'] = revenue_data['Report Date'].dt.strftime('%Y-Q%q')
    
    # Convert to millions for better display
    revenue_data['Revenue (Millions)'] = revenue_data['Revenue'] / 1000000
    revenue_data['Net Income (Millions)'] = revenue_data['Net Income'] / 1000000
    
    return revenue_data

def visualize_apple_earnings(earnings_data, revenue_data=None):
    """
    Create visualizations of Apple's quarterly earnings and revenue.
    
    Parameters:
    earnings_data (pandas.DataFrame): The quarterly earnings data
    revenue_data (pandas.DataFrame, optional): The quarterly revenue data
    """
    if revenue_data is not None:
        fig = plt.figure(figsize=(15, 15))
        num_rows = 3
    else:
        fig = plt.figure(figsize=(15, 10))
        num_rows = 2
    
    # EPS visualization
    plt.subplot(num_rows, 1, 1)
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
    plt.subplot(num_rows, 1, 2)
    colors = ['green' if x >= 0 else 'red' for x in earnings_data['Surprise(%)']]
    plt.bar(earnings_data['Quarter'], earnings_data['Surprise(%)'], color=colors)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    plt.title('Apple (AAPL) Earnings Surprise % Since 2015')
    plt.xlabel('Quarter')
    plt.ylabel('Surprise (%)')
    plt.xticks(rotation=90)
    plt.grid(True, alpha=0.3)
    
    # Revenue visualization (if data is available)
    if revenue_data is not None:
        plt.subplot(num_rows, 1, 3)
        plt.plot(revenue_data['Quarter'], revenue_data['Revenue (Millions)'], 'b-o', label='Revenue')
        plt.plot(revenue_data['Quarter'], revenue_data['Net Income (Millions)'], 'g-o', label='Net Income')
        plt.title('Apple (AAPL) Quarterly Revenue and Net Income Since 2015')
        plt.xlabel('Quarter')
        plt.ylabel('Amount ($ Millions)')
        plt.xticks(rotation=90)
        plt.legend()
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig("AAPL_earnings_since_2015.png")
    plt.show()

def display_apple_earnings_since_2015():
    """
    Display and analyze Apple's quarterly earnings since 2015.
    """
    # Try to get API key from environment variable or use the one in the script
    api_key = os.environ.get('FMP_API_KEY', API_KEY)
    
    if api_key == "YOUR_API_KEY":
        print("Please set your Financial Modeling Prep API key.")
        print("Sign up at https://financialmodelingprep.com/developer/docs/ to get a free API key.")
        print("Then replace 'YOUR_API_KEY' in the script or set it as an environment variable named FMP_API_KEY.")
        return
    
    print("Retrieving Apple (AAPL) quarterly earnings data since 2015...\n")
    
    # Get earnings data
    earnings_data = get_apple_earnings_since_2015(api_key)
    print(earnings_data)
    
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
    
    # Get revenue data if possible
    try:
        print("\nRetrieving Apple (AAPL) quarterly revenue data since 2015...\n")
        revenue_data = get_apple_quarterly_revenue_since_2015(api_key)
        
        if revenue_data is not None:
            print("\nQuarterly Revenue for Apple (AAPL) since 2015:")
            revenue_display = revenue_data[['Report Date', 'Quarter', 'Revenue (Millions)', 'Net Income (Millions)']]
            revenue_display = revenue_display.sort_values('Report Date', ascending=False)  # Show most recent first
            print(revenue_display)
    except Exception as e:
        print(f"Error retrieving revenue data: {e}")
        revenue_data = None
    
    # Create visualization
    visualize_apple_earnings(earnings_data.sort_values('Earnings Date'), revenue_data)

if __name__ == "__main__":
    display_apple_earnings_since_2015()
