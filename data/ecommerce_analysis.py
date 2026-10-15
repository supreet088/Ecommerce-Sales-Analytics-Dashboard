import pandas as pd

# Load products dataset
products = pd.read_csv("raw/products.csv")

# Display column names
print("Product Columns:")
print(products.columns.tolist())

# Display first five rows
print("\nFirst 5 Products:")
print(products.head())