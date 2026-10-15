import pandas as pd

sales = pd.read_csv(
    "processed/final_delivered_sales.csv"
)

regional = pd.read_csv(
    "processed/regional_sales.csv"
)

monthly = pd.read_csv(
    "processed/monthly_sales.csv"
)

print("===== DASHBOARD VALIDATION =====")

total = sales["sales"].sum()
regional_total = regional["total_revenue"].sum()
monthly_total = monthly["total_revenue"].sum()

print(f"Delivered Revenue: ₹{total:,.2f}")
print(f"Regional Revenue: ₹{regional_total:,.2f}")
print(f"Monthly Revenue: ₹{monthly_total:,.2f}")

print("\nRegional Totals Match:",
      abs(total - regional_total) < 0.01)

print("Monthly Totals Match:",
      abs(total - monthly_total) < 0.01)