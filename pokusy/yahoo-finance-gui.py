import tkinter as tk
from tkinter import ttk
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import numpy as np

class StockDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Market Data Viewer")
        self.root.geometry("1000x800")

        # Stock tickers to track
        self.tickers = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'META']

        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create Treeview frame
        self.table_frame = ttk.Frame(self.main_frame)
        self.table_frame.pack(fill=tk.X, expand=False)

        # Create Treeview
        self.tree = ttk.Treeview(self.table_frame, columns=(
            'Ticker', 'Current Price', 'Previous Close', 'Market Cap', 
            'PE Ratio', '52 Week High', '52 Week Low', 'Dividend Yield'
        ), show='headings', height=5)

        # Define headings
        headings = [
            'Ticker', 'Current Price', 'Previous Close', 'Market Cap', 
            'PE Ratio', '52 Week High', '52 Week Low', 'Dividend Yield'
        ]
        for heading in headings:
            self.tree.heading(heading, text=heading, command=lambda h=heading: self.sort_column(h, False))
            self.tree.column(heading, anchor='center', width=100)

        # Scrollbar for Treeview
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Layout Treeview and Scrollbar
        self.tree.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create graph frame
        self.graph_frame = ttk.Frame(self.main_frame)
        self.graph_frame.pack(fill=tk.BOTH, expand=True)

        # Create matplotlib figure
        self.figure, self.ax = plt.subplots(figsize=(10, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.graph_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        # Ticker selection dropdown for graph
        self.graph_ticker_var = tk.StringVar()
        self.graph_ticker_dropdown = ttk.Combobox(
            self.main_frame, 
            textvariable=self.graph_ticker_var, 
            values=self.tickers,
            state="readonly"
        )
        self.graph_ticker_dropdown.set(self.tickers[0])  # Default to first ticker
        self.graph_ticker_dropdown.pack(pady=5)
        self.graph_ticker_dropdown.bind('<<ComboboxSelected>>', self.update_graph)

        # Refresh button
        self.refresh_button = ttk.Button(self.main_frame, text="Refresh Data", command=self.update_stock_data)
        self.refresh_button.pack(pady=10)

        # Initially populate data
        self.stock_data = []
        self.update_stock_data()

    def fetch_stock_data(self):
        """
        Retrieve stock data for multiple tickers from Yahoo Finance.
        """
        stock_data = []
        stock_historical_data = {}
        
        for ticker in self.tickers:
            try:
                # Retrieve stock information
                stock = yf.Ticker(ticker)
                
                # Get historical market data
                hist = stock.history(period='1y')
                stock_historical_data[ticker] = hist
                
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
        
        return stock_data, stock_historical_data

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
                stock_data, historical_data = self.fetch_stock_data()
                
                # Update in main thread
                self.root.after(0, self.update_treeview, stock_data, historical_data)
            except Exception as e:
                print(f"Error updating stock data: {e}")
            finally:
                # Re-enable refresh button
                self.root.after(0, lambda: self.refresh_button.config(state=tk.NORMAL))
        
        # Start update in a separate thread
        threading.Thread(target=threaded_update, daemon=True).start()

    def update_treeview(self, stock_data, historical_data):
        """
        Update Treeview with fetched stock data
        """
        # Store historical data for graphing
        self.historical_data = historical_data
        
        # Clear any existing items
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Insert new data
        for data in stock_data:
            self.tree.insert('', 'end', values=tuple(data.values()))
        
        # Update graph with first ticker
        self.update_graph()

    def update_graph(self, event=None):
        """
        Update graph with selected ticker's price history
        """
        # Clear previous plot
        self.ax.clear()
        
        # Get selected ticker
        selected_ticker = self.graph_ticker_var.get()
        
        # Check if historical data exists
        if not hasattr(self, 'historical_data') or selected_ticker not in self.historical_data:
            return
        
        # Get historical data for selected ticker
        hist = self.historical_data[selected_ticker]
        
        # Plot close prices
        self.ax.plot(hist.index, hist['Close'], label=f'{selected_ticker} Close Price')
        self.ax.set_title(f'{selected_ticker} Stock Price Over Past Year')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Price ($)')
        self.ax.legend()
        
        # Rotate and align the tick labels
        self.figure.autofmt_xdate()
        
        # Refresh canvas
        self.canvas.draw()

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
