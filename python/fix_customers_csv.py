import pandas as pd

# read original file
df = pd.read_csv("../datasets/dim_customers.csv")

# save clean CSV
df.to_csv("../datasets/dim_customers_clean.csv", index=False)