import pandas as pd

# Load cleaned dataset
df = pd.read_csv("processed/final_delivered_sales.csv")

# Check missing sales
print("Missing Sales:", df["sales"].isna().sum())

# Check missing discounts
print("Missing Discounts:", df["discount_pct"].isna().sum())

# Check whether missing sales correspond to missing discounts
print("\nMissing Sales Records:")
print(
    df.loc[
        df["sales"].isna(),
        ["order_id", "quantity", "unit_price_inr", "discount_pct"]
    ].head(10)
)

# Calculate sales KPIs
total_revenue = df["sales"].sum()
total_profit = df["profit"].sum()

total_orders = df["order_id"].nunique()

# Count orders with valid sales
valid_orders = df.loc[
    df["sales"].notna(), "order_id"
].nunique()

average_order_value = total_revenue / valid_orders

print("\n===== SALES ANALYSIS =====")
print(f"Recorded Revenue: ₹{total_revenue:,.2f}")
print(f"Recorded Profit: ₹{total_profit:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Orders With Valid Sales: {valid_orders:,}")
print(f"Average Order Value (Valid Orders): ₹{average_order_value:,.2f}")


# Step 17: Category-wise Sales Analysis

category_sales = df.groupby("category")["sales"].sum()

category_sales = category_sales.sort_values(
    ascending=False
)

print("\n===== CATEGORY-WISE REVENUE =====")
print(category_sales)

# Category-wise profit
category_profit = df.groupby("category")["profit"].sum()

category_profit = category_profit.sort_values(
    ascending=False
)

print("\n===== CATEGORY-WISE PROFIT =====")
print(category_profit)


import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.bar(
    category_sales.index,
    category_sales.values,
    color="royalblue"
)

plt.title("Category-wise E-Commerce Revenue")
plt.xlabel("Product Category")
plt.ylabel("Revenue (INR)")

plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig("category_revenue.png", dpi=300)

plt.show()


# Step 18: Top 10 Products by Revenue

top_products = (
    df.groupby("product_name")["sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 PRODUCTS BY REVENUE =====")
print(top_products)


# Create Top 10 Products chart

plt.figure(figsize=(11, 6))

plt.barh(
    top_products.index,
    top_products.values,
    color="teal"
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Total Revenue (INR)")
plt.ylabel("Product Name")

# Highest revenue product at the top
plt.gca().invert_yaxis()

plt.tight_layout()

# Save chart
plt.savefig("top_10_products.png", dpi=300)

plt.show()



# Top 10 Products by Profit

top_profit_products = (
    df.groupby("product_name")["profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 PRODUCTS BY PROFIT =====")
print(top_profit_products)



# Top 10 Products by Quantity Sold

top_quantity_products = (
    df.groupby("product_name")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 PRODUCTS BY QUANTITY =====")
print(top_quantity_products)



# Save Top 10 Product Reports

from pathlib import Path

Path("processed").mkdir(exist_ok=True)

top_products.to_csv(
    "processed/top_10_revenue.csv",
    header=["total_revenue"]
)

top_profit_products.to_csv(
    "processed/top_10_profit.csv",
    header=["total_profit"]
)

top_quantity_products.to_csv(
    "processed/top_10_quantity.csv",
    header=["total_quantity"]
)

print("\nTop 10 product reports saved successfully!")



# Step 19: Monthly Sales Trend Analysis

monthly_sales = (
    df.groupby("order_month")["sales"]
    .sum()
    .sort_index()
)

print("\n===== MONTHLY SALES REPORT =====")
print(monthly_sales)

# Find highest revenue month
best_month = monthly_sales.idxmax()
best_revenue = monthly_sales.max()

print("\nHighest Revenue Month:", best_month)
print(f"Highest Monthly Revenue: ₹{best_revenue:,.2f}")


# Create monthly revenue chart

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o",
    color="royalblue"
)

plt.title("Monthly E-Commerce Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (INR)")

plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.savefig("monthly_sales_trend.png", dpi=300)

plt.show()


monthly_sales.to_csv(
    "processed/monthly_sales.csv",
    header=["total_revenue"]
)

print("\nMonthly sales report saved successfully!")