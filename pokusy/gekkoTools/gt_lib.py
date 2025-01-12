from pandas import DataFrame
import numpy as geek 

def invert_date_string(origDate: str) -> str:
    parts = origDate.split("-")
    parts.reverse()
    reversed_date = '-'.join(parts)
    return reversed_date   


def invert_date_strings(input_array: list[str]):
    output_array = []
    for orig_date in input_array:
        parts = orig_date.split("-")
        parts.reverse()
        reversed_date = '-'.join(parts)
        output_array.append(reversed_date)
    return output_array

def parse_euro_amount(amount_str):
    # Remove € symbol and any whitespace
    cleaned = amount_str.replace('€', '').strip()
    
    # Handle negative values (both -€ 55,62 and € -55,62 formats)
    is_negative = '-' in cleaned
    cleaned = cleaned.replace('-', '')
    
    # Replace comma with decimal point for float conversion
    cleaned = cleaned.replace(',', '.')
    
    # Convert to float and apply negative sign if needed
    number = float(cleaned)
    return -number if is_negative else number

def transform_dataframe_lynx(account: str, inDf: DataFrame):
    outDf = DataFrame(columns=("ACCOUNT","DATE","NAME","QUANTITY","PRICE","TOTAL"))    

    rows = inDf.shape[0]
    j = 0
    for i in range(1,rows):
        row = inDf.loc[i-1]  # Select the first row

        typ = row["Typ"]
        abs_quantity = row["Množství"]        

        if "STK" in typ and abs_quantity >=1:
            date = invert_date_string(row["Čas"].split(' ')[0])
            name = row["Název"]
            side = row["Strana"]

            price = parse_euro_amount(row["Cena"])
            quantity = -abs_quantity if "Prodej" in side  else abs_quantity
            total = quantity * price

            out_row = [ account, date, name, quantity, price, total]
            outDf.loc[j] = out_row
            j += 1
    
    return outDf


def transform_dataframe_degiro(account: str, inDf: DataFrame):
    outDf = DataFrame()
    
    rows = inDf.shape[0]
    accounts = geek.full((rows), account)

    outDf["ACCOUNT"] = accounts
    inv = invert_date_strings(inDf.get("Datum"))    
    outDf["DATE"] = inv
    outDf["NAME"] = inDf.get("Produkt")
    quantities = inDf.get("Počet")
    prices = inDf.get("Cena")
    outDf["QUANTITY"] = quantities
    outDf["PRICE"] = prices
    totals = geek.multiply(quantities, prices)  
    outDf["TOTAL"] = totals
    return outDf

def transform_dataframe_xtb(account: str, inDf: DataFrame):
    outDf = DataFrame()
    
    rows = inDf.shape[0]
    accounts = geek.full((rows), account)

    outDf["ACCOUNT"] = accounts
    inv = invert_date_strings(inDf.get("DATE"))
    outDf["DATE"] = inv
    outDf["NAME"] = inDf.get("SYMBOL")
    quantities = inDf.get("QUANTITY")
    prices = inDf.get("PRICE")
    outDf["QUANTITY"] = quantities
    outDf["PRICE"] = prices
    totals = geek.multiply(quantities, prices)  
    outDf["TOTAL"] = totals
    return outDf