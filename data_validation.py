import pandas as pd

df = pd.read_csv("processed/cleaned_orders.csv")

print("===== DATA VALIDATION =====")

print("Total Rows:", len(df))
print("Missing Discounts:", df["discount_pct"].isna().sum())
print("Missing Sales:", df["sales"].isna().sum())
print("Missing Profit:", df["profit"].isna().sum())

# Show records with missing discounts
missing = df[df["discount_pct"].isna()]

print("\n===== MISSING DISCOUNT RECORDS =====")
print(
    missing[
        ["order_id", "quantity",
         "unit_price_inr", "discount_pct"]
    ].head(10)
)

# Check order status
print("\n===== ORDER STATUS =====")
print(df["order_status"].value_counts())

# Check discount range
print("\n===== DISCOUNT STATISTICS =====")
print(df["discount_pct"].describe())


print("\n===== ORDER STATUS COUNTS =====")
print(df["order_status"].value_counts(dropna=False))

print("\n===== REVENUE BY ORDER STATUS =====")
print(
    df.groupby("order_status", dropna=False)["sales"]
    .agg(["count", "sum"])
)