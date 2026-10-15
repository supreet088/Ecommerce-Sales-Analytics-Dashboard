import pandas as pd
from pathlib import Path

# Load datasets
orders = pd.read_csv("processed/final_delivered_sales.csv")
customers = pd.read_csv("raw/customers.csv")

# Inspect customer columns
print("Customer Columns:")
print(customers.columns.tolist())

# Merge orders with customers
df = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one",
    indicator=True
)

print("\nMerged Dataset Shape:")
print(df.shape)

print("\nCustomer Matching Results:")
print(df["_merge"].value_counts())


# Top 10 customers by recorded spending
top_customers = (
    df.groupby("customer_id")["sales"]
    .sum(min_count=1)
    .sort_values(ascending=False)
    .head(10)
)

print("\n===== TOP 10 CUSTOMERS =====")
print(top_customers)


# Count orders placed by each customer
customer_orders = (
    df.groupby("customer_id")["order_id"]
    .nunique()
)

# Customers with more than one order
repeat_customers = customer_orders[
    customer_orders > 1
]

print("\n===== REPEAT CUSTOMER ANALYSIS =====")

print("Total Customers Who Ordered:", len(customer_orders))

print("Repeat Customers:", len(repeat_customers))

repeat_percentage = (
    len(repeat_customers) / len(customer_orders)
) * 100

print(f"Repeat Customer Percentage: {repeat_percentage:.2f}%")


import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.barh(
    top_customers.index.astype(str),
    top_customers.values,
    color="teal"
)

plt.gca().invert_yaxis()

plt.title("Top 10 Customers by Revenue")
plt.xlabel("Recorded Revenue (INR)")
plt.ylabel("Customer ID")

plt.tight_layout()

plt.savefig("top_10_customers.png", dpi=300)

plt.show()


Path("processed").mkdir(exist_ok=True)

top_customers.to_csv(
    "processed/top_10_customers.csv",
    header=["total_spending"]
)

customer_orders.to_csv(
    "processed/customer_order_counts.csv",
    header=["order_count"]
)

print("\nCustomer analysis reports saved successfully!")


