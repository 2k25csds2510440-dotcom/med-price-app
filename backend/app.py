from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware


# --------------------------------------------------
# APP
# --------------------------------------------------

app = FastAPI(
    title="Medicine Price Comparison API",
    description="Backend API for the medicine price comparison college project.",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------
# This allows our React frontend running on
# http://localhost:5173 to communicate with FastAPI.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# FILE LOCATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "final"
    / "synthetic_pharmacy_prices.csv"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"CSV file not found at: {DATA_FILE}"
    )

df = pd.read_csv(DATA_FILE)


# Remove completely empty rows
df = df.dropna(how="all")


# Clean column names
df.columns = [
    str(column).strip()
    for column in df.columns
]


# --------------------------------------------------
# PREPARE DATA
# --------------------------------------------------

# Our CSV uses "mrp" for the NPPA reference/ceiling
# value generated from the medicines seed data.
#
# We expose it from the API as:
# nppa_ceiling_price

if "mrp" in df.columns:
    df["nppa_ceiling_price"] = pd.to_numeric(
        df["mrp"],
        errors="coerce"
    )

if "price" in df.columns:
    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

if "discount_pct" in df.columns:
    df["discount_pct"] = pd.to_numeric(
        df["discount_pct"],
        errors="coerce"
    )


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------

def clean_record(record):
    """
    Convert pandas values into JSON-friendly values.
    """

    cleaned = {}

    for key, value in record.items():

        if pd.isna(value):
            cleaned[key] = None

        elif hasattr(value, "item"):
            cleaned[key] = value.item()

        else:
            cleaned[key] = value

    return cleaned


# --------------------------------------------------
# ROOT ENDPOINT
# --------------------------------------------------

@app.get("/")
def home():

    return {
        "message": "Medicine Price Comparison API is running",
        "docs": "/docs",
        "health": "/health"
    }


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "rows_loaded": len(df)
    }


# --------------------------------------------------
# ALL MEDICINES
# --------------------------------------------------

@app.get("/medicines")
def get_medicines():

    medicines = (
        df["medicine_name"]
        .dropna()
        .astype(str)
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return {
        "count": len(medicines),
        "medicines": medicines
    }


# --------------------------------------------------
# SEARCH MEDICINES
# --------------------------------------------------

@app.get("/search")
def search_medicine(
    q: str = Query(
        ...,
        min_length=1,
        description="Medicine name to search"
    )
):

    query = q.strip().lower()

    matches = df[
        df["medicine_name"]
        .astype(str)
        .str.lower()
        .str.contains(
            query,
            na=False,
            regex=False
        )
    ]

    return {
        "query": q,
        "count": len(matches),
        "results": [
            clean_record(record)
            for record in matches.to_dict(
                orient="records"
            )
        ]
    }


# --------------------------------------------------
# MEDICINE DETAILS
# --------------------------------------------------

@app.get("/medicine/{medicine_name}")
def medicine_details(
    medicine_name: str
):

    query = medicine_name.strip().lower()

    matches = df[
        df["medicine_name"]
        .astype(str)
        .str.lower()
        == query
    ]

    if matches.empty:

        return {
            "medicine_name": medicine_name,
            "count": 0,
            "results": []
        }

    return {
        "medicine_name": medicine_name,
        "count": len(matches),
        "results": [
            clean_record(record)
            for record in matches.to_dict(
                orient="records"
            )
        ]
    }