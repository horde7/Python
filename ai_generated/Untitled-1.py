#!/usr/bin/env python
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import certifi
import json

def get_jsonparsed_data(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)

url = ("https://financialmodelingprep.com/api/v3/search-name?query=META&limit=10&exchange=NASDAQ&apikey=RZ6QTubSErql5tnHU7wGy2jzyonyujsQ")
print(get_jsonparsed_data(url))