import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="E-Commerce Analytics",
    page_icon="📊",
    layout="wide"
)

st.title(":material/monitoring: E-Commerce Sales Dashboard")
st.caption("Delivered Orders | Sales & Customer Analytics")

# Load data
df = pd.read_csv("processed/final_delivered_sales.csv")

# Load customer location information
customers = pd.read_csv("raw/customers.csv")

# Add region information to sales dataset
if "region" not in df.columns:
    df = df.merge(
        customers[["customer_id", "region"]],
        on="customer_id",
        how="left",
        validate="many_to_one"
    )

# Sidebar filter
st.sidebar.header("Dashboard Filters")

categories = sorted(df["category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Product Categories",
    categories,
    default=categories
)


# Convert order_date to datetime before filtering
df["order_date"] = pd.to_datetime(df["order_date"])

# Apply category filter
filtered_df = df[
    df["category"].isin(selected_categories)
].copy()


# Step 34: Date Range Filter

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()

st.sidebar.subheader("Select Date Range")

date_range = st.sidebar.date_input(
    "Order Date",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        filtered_df["order_date"].dt.date.between(
            start_date, end_date
        )
    ].copy()


# Calculate KPIs
revenue = filtered_df["sales"].sum()
profit = filtered_df["profit"].sum()
orders = filtered_df["order_id"].nunique()

aov = revenue / orders if orders else 0
margin = profit / revenue * 100 if revenue else 0

# Display KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"₹{revenue/1e7:,.2f} Cr")
col2.metric("Gross Profit", f"₹{profit/1e7:,.2f} Cr")
col3.metric("Delivered Orders", f"{orders:,}")
col4.metric("Profit Margin", f"{margin:.2f}%")

st.divider()

# Category-wise revenue
category_sales = (
    filtered_df.groupby("category", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
)

fig1 = px.bar(
    category_sales,
    x="category",
    y="sales",
    title="Revenue by Product Category",
    labels={"sales": "Revenue (INR)", "category": "Category"}
)

# Monthly revenue
filtered_df = filtered_df.copy()
filtered_df["order_date"] = pd.to_datetime(
    filtered_df["order_date"]
)

monthly = (
    filtered_df.groupby(
        filtered_df["order_date"].dt.to_period("M")
    )["sales"]
    .sum()
    .reset_index()
)

monthly["order_date"] = monthly["order_date"].astype(str)

fig2 = px.line(
    monthly,
    x="order_date",
    y="sales",
    markers=True,
    title="Monthly Revenue Trend",
    labels={"order_date": "Month", "sales": "Revenue (INR)"}
)
fig2.update_xaxes(type="category")
left, right = st.columns(2)

with left:
    st.plotly_chart(fig1, width="stretch")

with right:
    st.plotly_chart(fig2, width="stretch")

st.divider()

st.subheader("Sales Data Preview")
st.dataframe(filtered_df.head(100), width="stretch")


# Region-wise Sales Analysis
st.divider()

st.subheader(":material/public: Regional Sales Analysis")

regional_sales = (
    filtered_df.groupby("region", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
)

fig3 = px.bar(
    regional_sales,
    x="region",
    y="sales",
    color="region",
    title="Revenue by Region",
    labels={
        "region": "Region",
        "sales": "Revenue (INR)"
    }
)

st.plotly_chart(fig3, width="stretch")



# Step 32: Filter-Aware Customer Segmentation

st.divider()
st.header(":material/groups: Customer Segmentation")

# Load saved customer segments
customer_segments = pd.read_csv(
    "processed/customer_segments.csv"
)

# Find customers who purchased selected categories
selected_customer_ids = filtered_df["customer_id"].dropna().unique()

# Keep segments for those customers
filtered_segments = customer_segments[
    customer_segments["customer_id"].isin(selected_customer_ids)
].copy()

# Count customers by segment
segment_counts = (
    filtered_segments["segment"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = ["Segment", "Customers"]

# Display chart
if not segment_counts.empty:
    fig4 = px.pie(
        segment_counts,
        names="Segment",
        values="Customers",
        title="Customer Segments for Selected Categories",
        hole=0.4
    )

    st.plotly_chart(fig4, width="stretch")
else:
    st.info("No customers found for selected categories.")

# Customer segment KPI cards
st.subheader("Customer Segment Summary")

high_value = (filtered_segments["segment"] == "High Value").sum()
medium_value = (filtered_segments["segment"] == "Medium Value").sum()
low_value = (filtered_segments["segment"] == "Low Value").sum()

col1, col2, col3 = st.columns(3)

col1.metric("High Value Customers", f"{high_value:,}")
col2.metric("Medium Value Customers", f"{medium_value:,}")
col3.metric("Low Value Customers", f"{low_value:,}")



# Step 33: Download Filtered Sales Data

st.divider()
st.subheader(":material/download: Download Sales Report")

# Convert filtered data into CSV format
csv_data = filtered_df.to_csv(index=False)

# Create download button
st.download_button(
    label="Download Filtered Sales Data",
    data=csv_data,
    file_name="filtered_ecommerce_sales.csv",
    mime="text/csv"
)



# Step 35: Automated Business Insights

st.divider()

st.subheader(":material/lightbulb: Automated Business Insights")

if not filtered_df.empty:

    # Top-selling product category
    top_category = (
        filtered_df.groupby("category")["sales"]
        .sum()
        .idxmax()
    )

    # Best-performing region
    top_region = (
        filtered_df.groupby("region")["sales"]
        .sum()
        .idxmax()
    )

    # Most profitable category
    profitable_category = (
        filtered_df.groupby("category")["profit"]
        .sum()
        .idxmax()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Top-Selling Category", top_category)
    col2.metric("Best-Performing Region", top_region)
    col3.metric("Most Profitable Category", profitable_category)

else:
    st.warning("No sales data available for the selected filters.")



# Step 35.2: Automated Business Recommendations

st.divider()

st.subheader(":material/recommend: Business Recommendations")

if not filtered_df.empty:

    # Calculate category performance
    category_performance = (
        filtered_df.groupby("category", as_index=False)
        .agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum")
        )
        .sort_values("revenue", ascending=False)
    )

    best_category = category_performance.iloc[0]["category"]
    lowest_category = category_performance.iloc[-1]["category"]

    # Calculate region performance
    region_performance = (
        filtered_df.groupby("region", as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )

    best_region = region_performance.iloc[0]["region"]

    st.success(
        f" {best_category} generates the highest revenue "
        "among the selected categories. Consider prioritizing "
        "inventory and marketing for this category."
    )

    st.info(
        f" {best_region} is the highest-revenue region. "
        "Investigate opportunities to strengthen sales "
        "and customer retention in this region."
    )

    if len(category_performance) > 1:
        st.warning(
            f" {lowest_category} generates the lowest revenue "
            "among the selected categories. Review product demand, "
            "pricing, and marketing performance."
        )

    # Profitability recommendation
    loss_categories = category_performance[
        category_performance["profit"] < 0
    ]

    if not loss_categories.empty:
        st.error(
            " Some product categories have negative total profit. "
            "Review their costs and pricing strategies."
        )
    else:
        st.info(
            " All selected product categories have "
            "non-negative total profit."
        )

else:
    st.warning("No data available to generate recommendations.")
