import pandas as pd

input_file = r"C:\Users\wellknow\Documents\med-price-app\data\final\nppa_combined.csv"
output_file = r"C:\Users\wellknow\Documents\med-price-app\data\final\nppa_cleaned.csv"

df = pd.read_csv(input_file, dtype=str)

print("Original rows:", len(df))

# Rename extracted NPPA columns
df = df.rename(columns={
    "1": "medicine_name",
    "2": "dosage",
    "3": "unit",
    "4": "nppa_ceiling_price"
})

# Remove empty medicine names
df = df[df["medicine_name"].notna()]

# Remove repeated header rows
df = df[
    df["medicine_name"].str.strip().str.lower() != "medicines"
]

# Clean medicine names
df["medicine_name"] = (
    df["medicine_name"]
    .astype(str)
    .str.replace(r"\\n", " ", regex=True)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# Clean dosage
df["dosage"] = (
    df["dosage"]
    .astype(str)
    .str.replace(r"\\n", " ", regex=True)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# Clean unit
df["unit"] = (
    df["unit"]
    .astype(str)
    .str.replace(r"\\n", " ", regex=True)
    .str.replace(r"\s+", " ", regex=True)
    .str.strip()
)

# Convert ceiling price to number
df["nppa_ceiling_price"] = pd.to_numeric(
    df["nppa_ceiling_price"],
    errors="coerce"
)

# Remove invalid prices
df = df[df["nppa_ceiling_price"].notna()]
df = df[df["nppa_ceiling_price"] > 0]

# Remove exact duplicate formulations
df = df.drop_duplicates(
    subset=[
        "medicine_name",
        "dosage",
        "unit",
        "nppa_ceiling_price"
    ]
)

# Temporary field — NOT a verified salt composition
df["salt_composition"] = df["medicine_name"]

# Keep required fields
df = df[
    [
        "medicine_name",
        "salt_composition",
        "dosage",
        "unit",
        "nppa_ceiling_price"
    ]
]

df = df.sort_values("medicine_name")

df.to_csv(output_file, index=False)

print("\nCLEANING COMPLETE!")
print("Clean rows:", len(df))

print("\nFirst 10 rows:")
print(df.head(10).to_string(index=False))

print("\nSaved to:")
print(output_file)
