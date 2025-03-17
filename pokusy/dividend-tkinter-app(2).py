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
        master.configure(bg='#2C3E50')

        # Sample dividend data
        self.data = pd.DataFrame({
            'Date': pd.date_range(start='1/1/2023', periods=6, freq='M'),
            'Dividend': [50.25, 52.75, 49.50, 55.00, 53.25, 56.50]
        })

        # Create Notebook (Tabs)
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Table Tab
        self.table_frame = ttk.Frame(self.notebook)
        self.create_table()
        self.notebook.add(self.table_frame, text='Table')

        # Graph Tab
        self.graph_frame = ttk.Frame(self.notebook)
        self.create_graph()
        self.notebook.add(self.graph_frame, text='Graph')

    def create_table(self):
        # Treeview Styling
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Dividend.Treeview', 
                        background='#34495E',
                        foreground='white',
                        fieldbackground='#34495E')
        style.map('Dividend.Treeview', 
                  background=[('selected', '#2980B9')])

        # Dividend Table
        tree = ttk.Treeview(self.table_frame, 
                            columns=('Date', 'Dividend'), 
                            show='headings', 
                            style='Dividend.Treeview')
        tree.heading('Date', text='Date')
        tree.heading('Dividend', text='Dividend ($)')
        tree.pack(expand=True, fill='both', padx=10, pady=10)

        for index, row in self.data.iterrows():
            tree.insert('', 'end', values=(row['Date'].strftime('%Y-%m'), f"{row['Dividend']:.2f}"))

    def create_graph(self):
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(6, 4), 
                                facecolor='#2C3E50',
                                edgecolor='white')
        ax.bar(self.data['Date'].dt.strftime('%Y-%m'), self.data['Dividend'], color='#2ECC71')
        ax.set_title('Monthly Dividends', color='white')
        ax.set_xlabel('Month', color='white')
        ax.set_ylabel('Dividend Amount ($)', color='white')
        ax.tick_params(colors='white')
        plt.xticks(rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill='both', padx=10, pady=10)

def main():
    root = tk.Tk()
    app = DividendApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
