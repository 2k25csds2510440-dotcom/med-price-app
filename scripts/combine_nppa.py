import pandas as pd
import glob
import os

input_folder = r"C:\Users\wellknow\Documents\med-price-app\data\extracted"

output_file = r"C:\Users\wellknow\Documents\med-price-app\data\final\nppa_combined.csv"

files = glob.glob(os.path.join(input_folder, "*.csv"))

print("CSV files found:", len(files))

dataframes = []

for file in files:
    print("Reading:", os.path.basename(file))

    try:
        df = pd.read_csv(file)
        df["source_file"] = os.path.basename(file)
        dataframes.append(df)

    except Exception as e:
        print("Could not read:", file)
        print("Error:", e)

if not dataframes:
    print("No CSV files found!")
    exit()

combined = pd.concat(dataframes, ignore_index=True)

print("\nCombined rows:", len(combined))

print("\nColumns found:")
print(combined.columns.tolist())

combined.to_csv(output_file, index=False)

print("\nSUCCESS!")
print("Saved to:")
print(output_file)
