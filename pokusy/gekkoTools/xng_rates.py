import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_exchange_rates(currency_pairs, period='6y'):
    """
    Download exchange rates for specified currency pairs
    """
    exchange_rates = {}
    
    for pair in currency_pairs:
        symbol = f"{pair}=X"
        try:
            data = yf.download(symbol, period=period)
            exchange_rates[pair] = data
            print(f"Successfully downloaded data for {pair}")
        except Exception as e:
            print(f"Error downloading {pair}: {e}")
    
    return exchange_rates

def calculate_monthly_averages(data):
    """
    Calculate monthly averages from daily data
    """
    monthly_avg = data.resample('M').mean()
    monthly_avg.index = monthly_avg.index.strftime('%Y-%m')
    return monthly_avg

# Define currency pairs
pairs = ['EURCZK', 'USDCZK', 'GBPCZK']

# Download exchange rates
print("Downloading 6 years of exchange rate data...")
rates = get_exchange_rates(pairs, period='10y')

# Create a DataFrame to store all monthly averages
all_monthly_averages = pd.DataFrame()

for pair, data in rates.items():
    if not data.empty:
        # Calculate monthly averages and round to 2 decimal places
        monthly_data = calculate_monthly_averages(data)
        all_monthly_averages[pair] = monthly_data['Close'].round(2)
        
        # Display last 5 months with proper formatting
        print(f"\n{pair} - Last 5 months:")
        print(all_monthly_averages[pair].tail().to_string(float_format=lambda x: '{:.2f}'.format(x)))

# Save to CSV with proper formatting
all_monthly_averages.to_csv('monthly_exchange_rates.csv', float_format='%.2f')
print("\nMonthly averages saved to 'monthly_exchange_rates.csv' with preserved decimal places")

# Display summary statistics for the entire period
print("\nSummary Statistics (6 Years):")
print("---------------------------")
for pair in pairs:
    if pair in all_monthly_averages.columns:
        stats = all_monthly_averages[pair].describe()
        print(f"\n{pair}:")
        print(f"Average Rate: {stats['mean']:.2f}")
        print(f"Minimum Rate: {stats['min']:.2f}")
        print(f"Maximum Rate: {stats['max']:.2f}")
        print(f"Standard Deviation: {stats['std']:.2f}")

# Calculate and display year-over-year changes
print("\nYear-over-Year Changes:")
print("---------------------")
for pair in pairs:
    if pair in all_monthly_averages.columns:
        current_avg = all_monthly_averages[pair].iloc[-1]
        year_ago_avg = all_monthly_averages[pair].iloc[-13]
        change = ((current_avg - year_ago_avg) / year_ago_avg) * 100
        print(f"{pair}: {change:.2f}%")