import pandas as pd

# Read the Excel file
try:
    df = pd.read_excel('car.xlsx')
    print('Columns:', df.columns.tolist())
    print('Shape:', df.shape)
    print('First few rows:')
    print(df.head())
except Exception as e:
    print('Error reading car.xlsx:', e) 