import pandas as pd
import os

# Input file
input_file = "data/final/nppa_combined.csv"

# Output file
output_file = "data/final/medicines_seed.csv"

# Read the NPPA data
df = pd.read_csv(input_file)

print("Original columns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

# Rename the NPPA columns
df = df.rename(columns={
    "0": "sl_no",
    "1": "medicine_name",
    "2": "dosage",
    "3": "unit",
    "4": "nppa_ceiling_price"
})

# Remove empty medicine names
df = df.dropna(subset=["medicine_name"])

# Convert medicine names to text
df["medicine_name"] = df["medicine_name"].astype(str).str.strip()

# Remove empty strings
df = df[df["medicine_name"] != ""]

# Create salt_composition as a placeholder
# The NPPA PDF does not provide a separately verified salt field.
df["salt_composition"] = df["medicine_name"]

# Keep only the columns required by our project
df = df[
    [
        "medicine_name",
        "salt_composition",
        "dosage",
        "nppa_ceiling_price"
    ]
]

# Remove duplicate medicines
df = df.drop_duplicates(
    subset=["medicine_name", "dosage"]
)

# Create output folder if needed
os.makedirs("data/final", exist_ok=True)

# Save the seed file
df.to_csv(output_file, index=False)

print("\nSeed file created successfully!")
print("Output:", output_file)
print("Total medicines:", len(df))