import pandas as pd

file_name = "PPR-2010-2025-Dublin-all-areas-estimated.csv"
df = pd.read_csv(file_name, low_memory=False)

date_column = "Date of Sale (dd/mm/yyyy)"
price_column = "Price (€)"
area_column = "square meters"

df[price_column] = (
    df[price_column]
    .astype("string")
    .str.replace("€", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)
df[price_column] = pd.to_numeric(df[price_column], errors="coerce")

df[area_column] = pd.to_numeric(df[area_column], errors="coerce")

for column in [price_column, area_column]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

print("Rows and columns:", df.shape)
print("Date range:", df[date_column].min(), "to", df[date_column].max())
print("Price summary:")
print(df[price_column].describe())
print("Area summary:")
print(df[area_column].describe())
print("Missing values:")
print(df[[date_column, price_column, area_column]].isna().sum())

print(
    df.nlargest(10, "Price (€)")[
        [
            "Date of Sale (dd/mm/yyyy)",
            "Address",
            "Price (€)",
            "Not Full Market Price",
            "VAT Exclusive",
            "Description of Property",
        ]
    ].to_string(index=False)
)

bulk_pattern = (
    r"\bblocks?\b|"
    r"\b\d+\s*-\s*\d+\b|"
    r"\b\d+\s+units?\b|"
    r"residential units|"
    r"apartment development|"
    r"commercial property"
)

address_column = "Address"

df["bulk_sale_review"] = (
    df[address_column]
    .astype("string")
    .str.contains(bulk_pattern, case=False, regex=True, na=False)
) | (df["Price (€)"] > 10_000_000)

review_columns = [
    "Address",
    "Price (€)",
    "Description of Property",
    "bulk_sale_review",
]

print("Rows flagged for review:", df["bulk_sale_review"].sum())
print(
    df.loc[df["bulk_sale_review"], review_columns]
    .head(20)
    .to_string(index=False)
)