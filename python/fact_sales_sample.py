import pandas as pd

df = pd.read_csv("../datasets/fact_sales.csv")
df.sample(5000).to_csv("../datasets/fact_sales_sample.csv", index=False)