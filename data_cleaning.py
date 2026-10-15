import pandas as pd

# Load messy dataset
df = pd.read_csv("data/messy_sales.csv")

print("Original Dataset:")
print(df)

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicates
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Fill missing Price with median price
df["Price"] = df["Price"].fillna(df["Price"].median())

# Fill missing Quantity with median quantity
df["Quantity"] = df["Quantity"].fillna(df["Quantity"].median())

print("\nMissing Values After Cleaning:")
print(df.isnull().sum())

# Remove duplicate rows
df = df.drop_duplicates()

print("\nDuplicate Rows After Cleaning:")
print(df.duplicated().sum())

# Find rows with negative prices
print("\nInvalid Prices:")
print(df[df["Price"] < 0])

# Replace invalid prices with missing values
df.loc[df["Price"] < 0, "Price"] = float("nan")

# Fill invalid prices using median of valid prices
df["Price"] = df["Price"].fillna(df["Price"].median())

# Save cleaned data
df.to_csv("data/cleaned_sales.csv", index=False)

print("\nCleaned dataset saved successfully!")


print("\nFinal Dataset:")
print(df)

print("\nFinal Missing Values:")
print(df.isnull().sum())

print("\nFinal Duplicates:")
print(df.duplicated().sum())

print("\nFinal Dataset Shape:")
print(df.shape)
