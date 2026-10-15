import pandas as pd
from pathlib import Path

# Step 1: Load cleaned data
df = pd.read_csv("processed/cleaned_orders.csv")

# Step 2: Check order status
print("===== ORDER STATUS =====")
print(df["order_status"].value_counts())

# Step 3: Keep only delivered orders
delivered = df[
    df["order_status"] == "Delivered"
].copy()

# Step 4: Calculate delivered sales KPIs
total_revenue = delivered["sales"].sum()
total_profit = delivered["profit"].sum()
total_orders = len(delivered)

average_order_value = total_revenue / total_orders

profit_margin = (
    total_profit / total_revenue * 100
    if total_revenue != 0 else 0
)

# Step 5: Display results
print("\n===== FINAL SALES KPIs =====")

print(f"Delivered Orders: {total_orders:,}")
print(f"Delivered Revenue: ₹{total_revenue:,.2f}")
print(f"Delivered Gross Profit: ₹{total_profit:,.2f}")
print(f"Average Order Value: ₹{average_order_value:,.2f}")
print(f"Gross Profit Margin: {profit_margin:.2f}%")

# Step 6: Save dataset
Path("processed").mkdir(exist_ok=True)

delivered.to_csv(
    "processed/final_delivered_sales.csv",
    index=False
)

print("\nFinal delivered sales dataset saved successfully!")


