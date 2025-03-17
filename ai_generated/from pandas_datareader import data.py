from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd

start_date = '2000-06-30'
end_date = '2020-06-30'

stocks = ['OMC','PUB','WPP','^IXIC']

panel_data = data.DataReader(stocks,'yahoo',start_date,end_date)
panel_data = panel_data[['Adj Close']]
print(panel_data)
panel_data.plot(y = 'Adj Close')
plt.show()