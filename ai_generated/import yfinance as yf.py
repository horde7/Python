import yfinance as yf
import pandas as pd

def get_index_tickers(index_symbol):
    """
    Retrieves the ticker symbols for a given stock market index.

    Args:
        index_symbol (str): The symbol of the index (e.g., "^GDAXI" for DAX, "^FTSE" for FTSE 100).

    Returns:
        list: A list of ticker symbols, or None if an error occurs.
    """
    try:
        index = yf.Ticker(index_symbol)
        # Handle different yfinance versions and index structures
        if hasattr(index.info, 'components'):
            components = index.info['components']
            if components is not None:
                return components
        elif hasattr(index, "get_components"): #For older yfinance version
            components = index.get_components()
            if components is not None:
                return components.tolist()
        else:
            print(f"Could not retrieve components for {index_symbol}. Check the index symbol or yfinance version.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_dax_tickers():
    """Retrieves DAX tickers."""
    return get_index_tickers("^GDAXI")

def get_ftse_tickers():
    """Retrieves FTSE 100 tickers."""
    return get_index_tickers("^FTSE")

# Example Usage:

dax_tickers = get_dax_tickers()
if dax_tickers:
    print("DAX Tickers:")
    for ticker in dax_tickers:
        print(ticker)

ftse_tickers = get_ftse_tickers()
if ftse_tickers:
    print("\nFTSE 100 Tickers:")
    for ticker in ftse_tickers:
        print(ticker)