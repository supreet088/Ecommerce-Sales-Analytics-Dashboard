import pandas as pd

# Load cleaned dataset
df = pd.read_csv("processed/final_delivered_sales.csv")

# Calculate customer spending
customer_spending = (
    df.groupby("customer_id")["sales"]
    .sum(min_count=1)
    .reset_index()
)

customer_spending.rename(
    columns={"sales": "total_spending"},
    inplace=True
)

print("Customer Spending:")
print(customer_spending.head())


# Create customer segments
def customer_segment(spending):
    if pd.isna(spending):
        return "Unknown"
    elif spending < 100000:
        return "Low Value"
    elif spending < 500000:
        return "Medium Value"
    else:
        return "High Value"

customer_spending["segment"] = (
    customer_spending["total_spending"]
    .apply(customer_segment)
)

print("\nCustomer Segments:")
print(customer_spending.head(10))


segment_counts = (
    customer_spending["segment"]
    .value_counts()
)

print("\n===== CUSTOMER SEGMENT COUNTS =====")
print(segment_counts)


import matplotlib.pyplot as plt

plt.figure(figsize=(8, 5))

plt.bar(
    segment_counts.index,
    segment_counts.values,
    color="steelblue"
)

plt.title("Customer Segmentation by Spending")
plt.xlabel("Customer Segment")
plt.ylabel("Number of Customers")

plt.tight_layout()

plt.savefig("customer_segments.png", dpi=300)

plt.show()


from pathlib import Path

Path("processed").mkdir(exist_ok=True)

customer_spending.to_csv(
    "processed/customer_segments.csv",
    index=False
)

print("\nCustomer segmentation report saved successfully!") 