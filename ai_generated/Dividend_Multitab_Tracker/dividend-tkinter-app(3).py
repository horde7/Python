import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DividendApp:
    def __init__(self, master):
        self.master = master
        master.title("Monthly Dividend Tracker")
        master.geometry("700x600")
        master.configure(bg='#2C3E50')

        # Conversion rates (example rates)
        self.usd_rate = 1.0
        self.eur_rate = 0.92
        self.czk_rate = 22.5

        # Sample dividend data in USD
        self.data = pd.DataFrame({
            'Date': pd.date_range(start='1/1/2023', periods=6, freq='M'),
            'Dividend_USD': [50.25, 52.75, 49.50, 55.00, 53.25, 56.50]
        })

        # Compute other currency columns
        self.data['Dividend_EUR'] = self.data['Dividend_USD'] * self.eur_rate
        self.data['Dividend_CZK'] = self.data['Dividend_USD'] * self.czk_rate

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Create tabs for each currency
        currencies = [
            ('USD', 'Dividend_USD', '#2ECC71'),
            ('EUR', 'Dividend_EUR', '#3498DB'),
            ('CZK', 'Dividend_CZK', '#E74C3C')
        ]

        for currency, column, color in currencies:
            tab_frame = ttk.Frame(self.notebook)
            self.create_tab(tab_frame, currency, column, color)
            self.notebook.add(tab_frame, text=currency)

    def create_tab(self, parent_frame, currency, column, bar_color):
        # Split frame into two parts
        top_frame = ttk.Frame(parent_frame)
        top_frame.pack(expand=True, fill='both')

        bottom_frame = ttk.Frame(parent_frame)
        bottom_frame.pack(expand=True, fill='both')

        # Table
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Dividend.Treeview', 
                        background='#34495E',
                        foreground='white',
                        fieldbackground='#34495E')
        style.map('Dividend.Treeview', 
                  background=[('selected', '#2980B9')])

        tree = ttk.Treeview(top_frame, 
                            columns=('Date', 'Dividend'), 
                            show='headings', 
                            style='Dividend.Treeview')
        tree.heading('Date', text='Date')
        tree.heading('Dividend', text=f'Dividend ({currency})')
        tree.pack(expand=True, fill='both', padx=10, pady=10)

        for _, row in self.data.iterrows():
            tree.insert('', 'end', values=(
                row['Date'].strftime('%Y-%m'), 
                f"{row[column]:.2f}"
            ))

        # Graph
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(6, 4), 
                                facecolor='#2C3E50',
                                edgecolor='white')
        ax.bar(self.data['Date'].dt.strftime('%Y-%m'), 
               self.data[column], 
               color=bar_color)
        ax.set_title(f'Monthly Dividends ({currency})', color='white')
        ax.set_xlabel('Month', color='white')
        ax.set_ylabel(f'Dividend Amount ({currency})', color='white')
        ax.tick_params(colors='white')
        plt.xticks(rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=bottom_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill='both', padx=10, pady=10)

def main():
    root = tk.Tk()
    app = DividendApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
