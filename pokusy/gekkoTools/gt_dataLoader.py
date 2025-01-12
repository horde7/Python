import pandas as pd
import subprocess
import gt_lib

#CSV_FILES_PATH = "RawBrokerData\\"
#CSV_FILES_PATH = "Data\\"
CSV_FILES_PATH = "d:\\Dropbox\\$Investing\\RawBrokerData\\"

dirParam = CSV_FILES_PATH + "*.csv"

# Spustí příkaz a získá výstup
result = subprocess.run(['dir', dirParam, '/b'], capture_output=True, text=True, shell=True)

# Rozdělí výstup na jednotlivé řádky a uloží je do pole
csvFiles = result.stdout.splitlines()

# Vytiskne seznam souborů jako řádky
print("\n".join(csvFiles));

df_list = []
df_total = pd.DataFrame()
for file in csvFiles:
    df = pd.read_csv(CSV_FILES_PATH +file)
    print(df)
    account = df["_ACCNT"] = file.split('_')[0]
    broker = account.split('-')[0]
    dfTrf: pd.DataFrame
    match broker:
        case "Lynx":
            df_list.append(gt_lib.transform_dataframe_lynx(account, df)) 
        case "Degiro":
            df_list.append(gt_lib.transform_dataframe_degiro(account, df)) 
        case "Xtb":
            df_list.append(gt_lib.transform_dataframe_xtb(account, df))
        case _:
            print(broker)    
    #df_list.append(df)
    #dfTrf = gt_lib.transform_dataframe_xtb(df)    
df_total = pd.concat(df_list, ignore_index=True)
sorted = df_total.sort_values(by=['DATE'])
# df_total = df_total.filter(items=["_ACCNT","DATE", "SYMBOL", "QUANTITY", "PRICE" ])
print (sorted)