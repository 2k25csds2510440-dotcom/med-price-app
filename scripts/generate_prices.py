import pandas as pd
import random

# Make the random prices reproducible
random.seed(42)

# Read medicine data
df = pd.read_csv(
    "data/final/medicines_seed.csv"
)

# Clean the NPPA price column
df["nppa_ceiling_price"] = pd.to_numeric(
    df["nppa_ceiling_price"],
    errors="coerce"
)

# Remove invalid rows such as "Ceiling price"
df = df.dropna(
    subset=["nppa_ceiling_price"]
)

# Demo pharmacies
dummy_pharmacies = [
    {
        "name": "Demo Pharmacy 1",
        "lat": 26.4499,
        "lng": 80.3319
    },
    {
        "name": "Demo Pharmacy 2",
        "lat": 26.4610,
        "lng": 80.3200
    },
    {
        "name": "Demo Pharmacy 3",
        "lat": 26.4700,
        "lng": 80.3400
    },
    {
        "name": "Demo Pharmacy 4",
        "lat": 26.4550,
        "lng": 80.3550
    },
    {
        "name": "Demo Pharmacy 5",
        "lat": 26.4480,
        "lng": 80.3100
    }
]

rows = []

# Generate pharmacy prices for every medicine
for _, med in df.iterrows():

    # Each medicine is available at 3–5 demo pharmacies
    chosen_pharmacies = random.sample(
        dummy_pharmacies,
        k=random.randint(3, 5)
    )

    for pharmacy in chosen_pharmacies:

        # Random discount between 0% and 30%
        discount = random.uniform(0, 0.30)

        # Calculate synthetic price
        price = round(
            float(med["nppa_ceiling_price"]) * (1 - discount),
            2
        )

        rows.append({
            "medicine_name": med["medicine_name"],
            "dosage": med["dosage"],
            "pharmacy_name": pharmacy["name"],
            "latitude": pharmacy["lat"],
            "longitude": pharmacy["lng"],
            "nppa_ceiling_price": round(
                float(med["nppa_ceiling_price"]),
                2
            ),
            "price": price,
            "discount_pct": round(
                discount * 100,
                1
            ),
            "is_synthetic": True
        })

# Create final table
result = pd.DataFrame(rows)

# Save CSV
result.to_csv(
    "data/final/synthetic_pharmacy_prices.csv",
    index=False
)

print("====================================")
print("Synthetic pharmacy prices generated!")
print("====================================")
print("Medicines:", len(df))
print("Generated rows:", len(result))
print("Output:")
print("data/final/synthetic_pharmacy_prices.csv")
print("====================================")