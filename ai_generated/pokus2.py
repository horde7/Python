import yfinance as yf
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_quarterly_financials(ticker_symbol):
    """
    Retrieves quarterly sales and earnings per share (EPS) data for a given ticker for the last 15 years.

    Args:
        ticker_symbol (str): The ticker symbol of the stock (e.g., "AAPL").

    Returns:
        tuple: A tuple containing two pandas DataFrames:
               - sales_df: DataFrame with quarterly sales data.
               - eps_df: DataFrame with quarterly EPS data.
               Returns (None, None) if an error occurs or data is unavailable.
    """
    try:
        ticker = yf.Ticker(ticker_symbol)

        # Get quarterly financials
        quarterly_financials = ticker.quarterly_financials
        if quarterly_financials.empty:
            print(f"No quarterly financials data available for {ticker_symbol}.")
            return None, None

        # Extract sales (totalRevenue) and EPS
        sales_data = quarterly_financials.loc["TotalRevenue"]
        eps_data = quarterly_financials.loc["BasicEPS"] #Or "DilutedEPS"

        # Convert to DataFrames and transpose for better readability
        sales_df = pd.DataFrame(sales_data).T
        eps_df = pd.DataFrame(eps_data).T

        # Format the index as dates
        sales_df.index = pd.to_datetime(sales_df.index)
        eps_df.index = pd.to_datetime(eps_df.index)

        # Filter for the last 15 years
        fifteen_years_ago = datetime.now() - relativedelta(years=5)
        sales_df = sales_df[sales_df.index >= fifteen_years_ago]
        eps_df = eps_df[eps_df.index >= fifteen_years_ago]

        return sales_df, eps_df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

# Example Usage:
ticker_symbol = "MSFT"  # Example: Microsoft
sales_df, eps_df = get_quarterly_financials(ticker_symbol)

if sales_df is not None and eps_df is not None:
    print(f"Quarterly Sales (Last 15 Years) for {ticker_symbol}:")
    print(sales_df)

    print(f"\nQuarterly EPS (Last 15 Years) for {ticker_symbol}:")
    print(eps_df)