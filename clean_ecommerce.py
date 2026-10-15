import pandas as pd
from pathlib import Path

# Step 1: Load datasets
orders = pd.read_csv("raw/orders.csv")
products = pd.read_csv("raw/products.csv")

print("Original Orders:", orders.shape)

# Step 2: Remove exact duplicates
orders = orders.drop_duplicates().copy()

# Step 3: Handle missing payment methods
orders["payment_method"] = orders["payment_method"].fillna("Unknown")

# Step 4: Convert columns to correct data types
orders["order_date"] = pd.to_datetime(
    orders["order_date"], errors="coerce"
)

orders["discount_pct"] = pd.to_numeric(
    orders["discount_pct"], errors="coerce"
)

# Step 5: Combine orders and products
df = orders.merge(
    products,
    on="product_id",
    how="left",
    validate="many_to_one"
)

print("\nMerged Dataset Shape:", df.shape)

# Step 6: Check missing product information
print("\nMissing Product Prices:")
print(df["unit_price_inr"].isna().sum())

# Step 7: Calculate sales and profit
# First check whether discount is stored as 10 or 0.10
print("\nDiscount Values:")
print(df["discount_pct"].describe())

# Identify originally missing discounts
df["discount_was_missing"] = df["discount_pct"].isna()

# Calculate median discount
median_discount = df["discount_pct"].median()

# Fill missing discounts with the median
df["discount_pct"] = df["discount_pct"].fillna(
    median_discount
)

print("Estimated Missing Discounts:",
      df["discount_was_missing"].sum())

print("Median Discount Used:", median_discount)

# This dataset uses percentages such as 10 for 10%.
discount_rate = df["discount_pct"]

df["sales"] = (
    df["quantity"]
    * df["unit_price_inr"]
    * (1 - discount_rate)
)

df["profit"] = (
    df["sales"]
    - df["quantity"] * df["unit_cost_inr"]
)

# Step 8: Create year and month columns
df["order_year"] = df["order_date"].dt.year

df["order_month"] = (
    df["order_date"].dt.to_period("M").astype(str)
)

# Step 9: Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Step 10: Save cleaned dataset
Path("processed").mkdir(exist_ok=True)

df.to_csv(
    "processed/cleaned_orders.csv",
    index=False
)

print("\nFinal Dataset Shape:", df.shape)
print("Cleaned dataset saved successfully!")