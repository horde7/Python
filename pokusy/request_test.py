import requests as r

link = "https://query1.finance.yahoo.com/v7/finance/download/ISPA.DE?period1=946682256&period2=1804064656&interval=1d&events=div&includeAdjustedClose=true"
resp = r.get(link, headers = {'User-agent': 'your bot 0.1'})

print(resp.status_code)
print(resp)
print(resp.text)

input()