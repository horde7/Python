import tkinter as tk
from tkinter import ttk
import yfinance as yf
import pandas as pd
import threading

class StockDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Market Data Viewer")
        self.root.geometry("800x600")

        # Stock tickers to track
        self.tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']

        # Create main frame
        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create Treeview
        self.tree = ttk.Treeview(self.frame, columns=(
            'Ticker', 'Current Price', 'Previous Close', 'Market Cap', 
            'PE Ratio', '52 Week High', '52 Week Low', 'Dividend Yield'
        ), show='headings')

        # Define headings
        headings = [
            'Ticker', 'Current Price', 'Previous Close', 'Market Cap', 
            'PE Ratio', '52 Week High', '52 Week Low', 'Dividend Yield'
        ]
        for heading in headings:
            self.tree.heading(heading, text=heading, command=lambda h=heading: self.sort_column(h, False))
            self.tree.column(heading, anchor='center', width=100)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Layout Treeview and Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Refresh button
        self.refresh_button = ttk.Button(root, text="Refresh Data", command=self.update_stock_data)
        self.refresh_button.pack(pady=10)

        # Initially populate data
        self.update_stock_data()

    def fetch_stock_data(self):
        """
        Retrieve stock data for multiple tickers from Yahoo Finance.
        """
        stock_data = []
        
        for ticker in self.tickers:
            try:
                # Retrieve stock information
                stock = yf.Ticker(ticker)
                
                # Get historical market data
                hist = stock.history(period='1mo')
                
                # Get fundamental data
                info = stock.info
                
                # Extract key metrics
                data_entry = {
                    'Ticker': ticker,
                    'Current Price': f"${hist['Close'][-1]:.2f}" if not hist.empty else 'N/A',
                    'Previous Close': f"${hist['Close'][-2]:.2f}" if len(hist) > 1 else 'N/A',
                    'Market Cap': self.format_market_cap(info.get('marketCap', 'N/A')),
                    'PE Ratio': f"{info.get('trailingPE', 'N/A'):.2f}" if isinstance(info.get('trailingPE'), (int, float)) else 'N/A',
                    '52 Week High': f"${info.get('fiftyTwoWeekHigh', 'N/A'):.2f}",
                    '52 Week Low': f"${info.get('fiftyTwoWeekLow', 'N/A'):.2f}",
                    'Dividend Yield': f"{(info.get('dividendYield', 0) * 100):.2f}%" if isinstance(info.get('dividendYield'), float) else 'N/A'
                }
                
                stock_data.append(data_entry)
            except Exception as e:
                print(f"Error fetching data for {ticker}: {e}")
        
        return stock_data

    def update_stock_data(self):
        """
        Update the Treeview with latest stock data in a separate thread
        """
        # Disable refresh button during update
        self.refresh_button.config(state=tk.DISABLED)
        
        # Clear existing items
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Show loading
        self.tree.insert('', 'end', values=('Loading data...', '', '', '', '', '', '', ''))
        
        def threaded_update():
            try:
                # Fetch data
                stock_data = self.fetch_stock_data()
                
                # Clear loading and update in main thread
                self.root.after(0, self.update_treeview, stock_data)
            except Exception as e:
                print(f"Error updating stock data: {e}")
            finally:
                # Re-enable refresh button
                self.root.after(0, lambda: self.refresh_button.config(state=tk.NORMAL))
        
        # Start update in a separate thread
        threading.Thread(target=threaded_update, daemon=True).start()

    def update_treeview(self, stock_data):
        """
        Update Treeview with fetched stock data
        """
        # Clear any existing items
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Insert new data
        for data in stock_data:
            self.tree.insert('', 'end', values=tuple(data.values()))

    def format_market_cap(self, market_cap):
        """
        Format market cap with appropriate abbreviation
        """
        if isinstance(market_cap, (int, float)):
            if market_cap >= 1_000_000_000:
                return f"${market_cap/1_000_000_000:.2f}B"
            elif market_cap >= 1_000_000:
                return f"${market_cap/1_000_000:.2f}M"
        return str(market_cap)

    def sort_column(self, column, reverse):
        """
        Sort the treeview column
        """
        # Get column data
        l = [(self.tree.set(k, column), k) for k in self.tree.get_children('')]
        
        # Try to convert to float for numeric sorting
        try:
            l = [(float(x.replace('$','').replace('%','').replace('B','').replace('M','')), k) for x, k in l]
            l.sort(reverse=reverse)
        except ValueError:
            # If conversion fails, do string sorting
            l.sort(reverse=reverse)
        
        # Rearrange items
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        
        # Toggle sort direction
        self.tree.heading(column, command=lambda: self.sort_column(column, not reverse))

def main():
    root = tk.Tk()
    app = StockDataApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()