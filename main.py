import pandas as pd
df = pd.read_csv("data/sales.csv")
df["Sales"] = df["Price"] * df["Quantity"]
print(df)
total_revenue = df["Sales"].sum()
print("Total Sales Revenue: ₹", total_revenue)
product_sales = df.groupby("Product")["Sales"].sum()
product_sales = product_sales.sort_values(ascending=False)
print("\nProduct-wise Revenue:")
print(product_sales)
product_quantity = df.groupby("Product")["Quantity"].sum()
product_quantity = product_quantity.sort_values(ascending=False)
print("\nProduct-wise Quantity Sold:")
print(product_quantity)
category_sales = df.groupby("Category")["Sales"].sum()
category_sales = category_sales.sort_values(ascending=False)
print("\nCategory-wise Revenue:")
print(category_sales)
category_percentage = (category_sales / total_revenue) * 100
category_percentage = category_percentage.round(2)
print("\nCategory Revenue Percentage: ")
print(category_percentage) 

# Creating Bar Graph
import matplotlib.pyplot as plt
plt.bar(category_sales.index, category_sales.values)
plt.title("Category-wise Sales Revenue")
plt.xlabel("Product Category")
plt.ylabel("Sales Revenue (INR)")
plt.show()

# Creating Pychart
plt.figure(figsize=(7, 7))
plt.pie(
    category_sales.values,
    labels=category_sales.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Revenue Distribution by Category")
plt.show()