import pandas as pd

# Load customers dataset
customers = pd.read_csv("raw/customers.csv")

# Display column names
print("===== CUSTOMER DATASET COLUMNS =====")
print(customers.columns.tolist())

# Display first five customers
print("\n===== FIRST 5 CUSTOMERS =====")
print(customers.head())

# Check missing values
print("\n===== MISSING VALUES =====")
print(customers.isnull().sum())


# Step 22: Regional Sales Analysis

# Load cleaned orders
orders = pd.read_csv("processed/final_delivered_sales.csv")

# Merge orders with customer location data
df = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one"
)

print("\n===== MERGED DATASET =====")
print("Rows and Columns:", df.shape)

# Check whether any customer locations are missing
print("Missing Regions:", df["region"].isna().sum())
print("Missing Cities:", df["city"].isna().sum())


# Calculate revenue by region
regional_sales = (
    df.groupby("region")["sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n===== REGION-WISE REVENUE =====")
print(regional_sales)

# Find highest revenue region
best_region = regional_sales.idxmax()

print("\nHighest Revenue Region:", best_region)


# Calculate revenue by city
city_sales = (
    df.groupby(["region", "city"])["sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\n===== TOP 10 CITIES BY REVENUE =====")
print(city_sales.head(10))


# Calculate profit by region
regional_profit = (
    df.groupby("region")["profit"]
    .sum()
    .sort_values(ascending=False)
)

print("\n===== REGION-WISE PROFIT =====")
print(regional_profit)


import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.bar(
    regional_sales.index,
    regional_sales.values,
    color="royalblue"
)

plt.title("Region-Wise E-Commerce Revenue")
plt.xlabel("Region")
plt.ylabel("Recorded Revenue (INR)")

plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig("regional_revenue.png", dpi=300)

plt.show()


from pathlib import Path

Path("processed").mkdir(exist_ok=True)

regional_sales.to_csv(
    "processed/regional_sales.csv",
    header=["total_revenue"]
)

regional_profit.to_csv(
    "processed/regional_profit.csv",
    header=["total_profit"]
)

city_sales.to_csv(
    "processed/city_sales.csv",
    header=["total_revenue"]
)

print("\nRegional analysis reports saved successfully!")