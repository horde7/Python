import tkinter as tk
from tkinter import ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DividendApp:
    def __init__(self, master):
        self.master = master
        master.title("Monthly Dividend Tracker")
        master.geometry("600x500")

        # Sample dividend data
        self.data = pd.DataFrame({
            'Date': pd.date_range(start='1/1/2023', periods=6, freq='M'),
            'Dividend': [50.25, 52.75, 49.50, 55.00, 53.25, 56.50]
        })

        self.create_widgets()

    def create_widgets(self):
        # Dividend Table
        self.tree = ttk.Treeview(self.master, columns=('Date', 'Dividend'), show='headings')
        self.tree.heading('Date', text='Date')
        self.tree.heading('Dividend', text='Dividend ($)')
        self.tree.pack(pady=10, padx=10, fill=tk.X)

        for index, row in self.data.iterrows():
            self.tree.insert('', 'end', values=(row['Date'].strftime('%Y-%m'), f"{row['Dividend']:.2f}"))

        # Create Matplotlib Figure
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(self.data['Date'].dt.strftime('%Y-%m'), self.data['Dividend'], color='green')
        ax.set_title('Monthly Dividends')
        ax.set_xlabel('Month')
        ax.set_ylabel('Dividend Amount ($)')
        plt.xticks(rotation=45)

        # Embed Matplotlib Figure in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

def main():
    root = tk.Tk()
    app = DividendApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
