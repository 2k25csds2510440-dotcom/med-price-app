import pandas as pd

input_file = r"C:\Users\wellknow\Documents\med-price-app\data\final\nppa_cleaned.csv"
output_file = r"C:\Users\wellknow\Documents\med-price-app\data\final\medicines_seed.csv"

df = pd.read_csv(input_file)

# Common medicines we want to prioritize for the demo
preferred_medicines = [
    "Paracetamol",
    "Metformin",
    "Atorvastatin",
    "Amlodipine",
    "Losartan",
    "Telmisartan",
    "Pantoprazole",
    "Omeprazole",
    "Amoxicillin",
    "Azithromycin",
    "Cefixime",
    "Ciprofloxacin",
    "Doxycycline",
    "Metronidazole",
    "Albendazole",
    "Acyclovir",
    "Aspirin",
    "Clopidogrel",
    "Ibuprofen",
    "Diclofenac",
    "Aceclofenac",
    "Cetirizine",
    "Levocetirizine",
    "Loratadine",
    "Fexofenadine",
    "Montelukast",
    "Salbutamol",
    "Budesonide",
    "Prednisolone",
    "Dexamethasone",
    "Ondansetron",
    "Domperidone",
    "Loperamide",
    "ORS",
    "Calcium",
    "Vitamin",
    "Iron",
    "Folic Acid",
    "Insulin",
    "Glimepiride",
    "Gliclazide",
    "Sitagliptin",
    "Pioglitazone",
    "Rosuvastatin",
    "Simvastatin",
    "Enalapril",
    "Ramipril",
    "Atenolol",
    "Metoprolol",
    "Propranolol",
    "Furosemide",
    "Hydrochlorothiazide",
    "Spironolactone",
    "Levothyroxine",
    "Fluconazole",
    "Clotrimazole",
    "Miconazole",
    "Permethrin",
    "Hydrocortisone",
    "Betamethasone",
    "Amikacin",
    "Gentamicin",
    "Ceftriaxone",
    "Cefotaxime",
    "Levofloxacin",
    "Ofloxacin",
    "Moxifloxacin",
    "Rifampicin",
    "Isoniazid",
    "Ethambutol",
    "Pyrazinamide",
    "Artemether",
    "Artesunate",
    "Chloroquine",
    "Primaquine",
    "Tinidazole",
    "Albendazole",
    "Mebendazole",
    "Famotidine",
    "Ranitidine",
    "Rabeprazole",
    "Esomeprazole",
    "Lansoprazole",
    "Drotaverine",
    "Hyoscine",
    "Tramadol",
    "Morphine",
    "Lidocaine",
    "Adrenaline",
    "Atropine",
    "Adenosine",
    "Digoxin",
    "Nitroglycerin",
    "Warfarin",
    "Heparin",
    "Enoxaparin",
    "Vitamin K",
    "Magnesium",
    "Potassium",
    "Sodium",
    "Zinc",
    "Calamine",
    "Povidone",
    "Chlorhexidine",
    "Hydrogen Peroxide",
    "Amoxicillin",
    "Ampicillin",
    "Cloxacillin",
    "Flucloxacillin",
    "Linezolid",
    "Vancomycin",
    "Meropenem",
    "Piperacillin",
    "Tazobactam",
    "Nystatin",
    "Ketoconazole",
    "Terbinafine",
    "Acyclovir",
    "Valacyclovir",
    "Oseltamivir",
    "Acetylsalicylic",
    "Naproxen",
    "Ketorolac",
    "Meloxicam",
    "Indomethacin",
    "Allopurinol",
    "Colchicine",
    "Tamsulosin",
    "Finasteride",
    "Sildenafil",
    "Bisacodyl",
    "Lactulose",
    "Senna",
    "Omeprazole",
    "Prednisolone",
    "Cetrizine",
    "Theophylline"
]

# Make a copy
df["medicine_lower"] = df["medicine_name"].astype(str).str.lower()

# First select medicines matching our preferred list
selected = pd.DataFrame()

for medicine in preferred_medicines:
    matches = df[
        df["medicine_lower"].str.contains(
            medicine.lower(),
            regex=False,
            na=False
        )
    ]

    selected = pd.concat(
        [selected, matches],
        ignore_index=True
    )

# Remove duplicate formulations
selected = selected.drop_duplicates(
    subset=[
        "medicine_name",
        "dosage",
        "unit",
        "nppa_ceiling_price"
    ]
)

# If fewer than 150 were found, fill with other NPPA medicines
if len(selected) < 150:
    remaining = df[
        ~df.index.isin(selected.index)
    ]

    selected = pd.concat(
        [selected, remaining],
        ignore_index=True
    )

# Keep maximum 150 rows
selected = selected.head(150)

# Keep the columns needed by the project
selected = selected[
    [
        "medicine_name",
        "salt_composition",
        "dosage",
        "nppa_ceiling_price"
    ]
]

# Save
selected.to_csv(
    output_file,
    index=False
)

print("SUCCESS!")
print("Medicines selected:", len(selected))
print("\nFirst 20 medicines:")
print(selected.head(20).to_string(index=False))
print("\nSaved to:")
print(output_file)
