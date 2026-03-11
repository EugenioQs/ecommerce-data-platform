import pandas as pd

# Load dataset
df = pd.read_csv("../datasets/orders.csv")

print("\nDATASET SHAPE")
print(df.shape)

print("\nCOLUMN NAMES")
print(df.columns)

print("\nDATA TYPES")
print(df.dtypes)

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nFIRST 10 ROWS")
print(df.head(10))

# Revenue column
df["revenue"] = df["quantity"] * df["unitprice"]

print("\nTOTAL REVENUE")
print(df["revenue"].sum())

print("\nREVENUE BY COUNTRY")
revenue_country = df.groupby("country")["revenue"].sum().sort_values(ascending=False)
print(revenue_country.head(10))

print("\nNEGATIVE QUANTITIES (RETURNS)")
print(df[df["quantity"] < 0].shape)

print("\nZERO OR NEGATIVE PRICES")
print(df[df["unitprice"] <= 0].shape)