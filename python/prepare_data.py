import pandas as pd

df = pd.read_excel("../datasets/online_retail.xlsx")

df.columns = df.columns.str.lower().str.replace(" ", "_")

df.to_csv("../datasets/orders.csv", index=False)

print("Dataset converted successfully")