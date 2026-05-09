import pandas as pd
import sys

# Read the Excel file
file_path = r'C:\Python_lian_xi\Test.xlsx'

try:
    # Load the Excel file
    df = pd.read_excel(file_path)
    
    print("=" * 80)
    print("FILE CONTENTS:")
    print("=" * 80)
    print(df)
    
    print("\n" + "=" * 80)
    print("COLUMN NAMES:")
    print("=" * 80)
    print(df.columns.tolist())
    
    print("\n" + "=" * 80)
    print("DATA TYPES:")
    print("=" * 80)
    print(df.dtypes)
    
    print("\n" + "=" * 80)
    print("DATA SUMMARY (info):")
    print("=" * 80)
    df.info()
    
    print("\n" + "=" * 80)
    print("STATISTICAL SUMMARY (describe):")
    print("=" * 80)
    print(df.describe())
    
    print("\n" + "=" * 80)
    print("SHAPE: {} rows, {} columns".format(df.shape[0], df.shape[1]))
    print("=" * 80)
    
except Exception as e:
    print(f"Error reading file: {e}")
    sys.exit(1)
