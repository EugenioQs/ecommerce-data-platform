import pandas as pd

print("Loading dataset...")

# Load dataset
df = pd.read_csv("../datasets/orders.csv")

# Convert date column
df["invoicedate"] = pd.to_datetime(df["invoicedate"])

# Create revenue column
df["revenue"] = df["quantity"] * df["unitprice"]

print("Creating dimension tables...")

# -----------------------------
# PRODUCT DIMENSION
# -----------------------------
dim_products = df[["stockcode", "description"]].drop_duplicates()

dim_products["product_id"] = range(1, len(dim_products) + 1)

dim_products = dim_products[["product_id", "stockcode", "description"]]

# -----------------------------
# CUSTOMER DIMENSION
# -----------------------------
dim_customers = df[["customerid"]].drop_duplicates()

dim_customers = dim_customers.rename(columns={
    "customerid": "customer_id"
})

# -----------------------------
# COUNTRY DIMENSION
# -----------------------------
dim_country = df[["country"]].drop_duplicates()

dim_country["country_id"] = range(1, len(dim_country) + 1)

dim_country = dim_country[["country_id", "country"]]

# -----------------------------
# DATE DIMENSION
# -----------------------------
df["date"] = pd.to_datetime(df["invoicedate"]).dt.normalize()

dim_date = pd.DataFrame()

dim_date["date"] = pd.to_datetime(df["date"].unique())
dim_date["date"] = dim_date["date"].dt.normalize()

dim_date["date_id"] = range(1, len(dim_date) + 1)

dim_date["year"] = dim_date["date"].dt.year
dim_date["month"] = dim_date["date"].dt.month
dim_date["day"] = dim_date["date"].dt.day
dim_date["weekday"] = dim_date["date"].dt.day_name()

print("Saving dimension tables...")

dim_products.to_csv("../datasets/dim_products.csv", index=False)
dim_customers.to_csv("../datasets/dim_customers.csv", index=False)
dim_country.to_csv("../datasets/dim_country.csv", index=False)
dim_date.to_csv("../datasets/dim_date.csv", index=False)

print("Dimension tables created")

# -----------------------------
# BUILD FACT TABLE
# -----------------------------
print("Building fact table...")

# Merge product ids
fact = df.merge(dim_products, on=["stockcode", "description"], how="left")

# Merge country ids
fact = fact.merge(dim_country, on="country", how="left")

# Merge date ids
fact = fact.merge(dim_date, on="date", how="left")

# Select fact columns
fact_sales = fact[[
    "invoiceno",
    "product_id",
    "customerid",
    "country_id",
    "date_id",
    "quantity",
    "unitprice",
    "revenue"
]]

# Rename columns for warehouse standard
fact_sales = fact_sales.rename(columns={
    "invoiceno": "invoice_no",
    "customerid": "customer_id",
    "unitprice": "unit_price"
})

# Save fact table
fact_sales.to_csv("../datasets/fact_sales.csv", index=False)

print("Fact table created successfully!")

print("\nSTAR SCHEMA DATASETS CREATED:")
print("- dim_products.csv")
print("- dim_customers.csv")
print("- dim_country.csv")
print("- dim_date.csv")
print("- fact_sales.csv")