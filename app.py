import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


DATA_PATH = Path("data/ecommerce_orders.csv")

st.set_page_config(page_title="E-Commerce Analytics", layout="wide")


@st.cache_data
def load_orders():
    orders = pd.read_csv(DATA_PATH, parse_dates=["invoice_date"])
    orders["invoice_month"] = orders["invoice_date"].dt.to_period("M").astype(str)
    return orders


def money(value):
    return f"${value:,.0f}"


def build_connection(orders):
    conn = sqlite3.connect(":memory:")
    orders.to_sql("orders", conn, index=False, if_exists="replace")
    return conn


def customer_segments(orders):
    snapshot = orders["invoice_date"].max() + pd.Timedelta(days=1)
    rfm = orders.groupby("customer_id").agg(
        recency=("invoice_date", lambda x: (snapshot - x.max()).days),
        frequency=("invoice_no", "nunique"),
        monetary=("revenue", "sum"),
        estimated_profit=("estimated_profit", "sum"),
    )
    rfm["value_segment"] = pd.qcut(
        rfm["monetary"].rank(method="first"),
        q=4,
        labels=["Low Value", "Developing", "Loyal", "VIP"],
    )
    rfm["retention_segment"] = pd.cut(
        rfm["recency"],
        bins=[-1, 30, 90, 180, 9999],
        labels=["Active", "Warm", "At Risk", "Dormant"],
    )
    return rfm.reset_index()


def bar_chart(data, x, y, title):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=data, x=x, y=y, hue=x, ax=ax, palette="viridis", legend=False)
    ax.set_title(title)
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(rotation=25, ha="right")
    st.pyplot(fig, clear_figure=True)


orders = load_orders()
conn = build_connection(orders)

st.title("E-Commerce Customer Analytics Dashboard")
st.caption(
    "Executive dashboard built on the UCI Online Retail dataset. "
    "Profit is estimated because the source dataset does not include cost of goods sold."
)

with st.sidebar:
    st.header("Filters")
    min_date, max_date = orders["invoice_date"].dt.date.min(), orders["invoice_date"].dt.date.max()
    date_range = st.date_input("Invoice date range", value=(min_date, max_date))
    countries = st.multiselect(
        "Country",
        sorted(orders["country"].unique()),
        default=["United Kingdom"] if "United Kingdom" in set(orders["country"]) else sorted(orders["country"].unique())[:5],
    )
    categories = st.multiselect(
        "Product category",
        sorted(orders["product_category"].unique()),
        default=sorted(orders["product_category"].unique()),
    )

filtered = orders[
    (orders["invoice_date"].dt.date >= date_range[0])
    & (orders["invoice_date"].dt.date <= date_range[1])
    & (orders["country"].isin(countries))
    & (orders["product_category"].isin(categories))
]

customer_orders = filtered.groupby("customer_id")["invoice_no"].nunique()
revenue = filtered["revenue"].sum()
estimated_profit = filtered["estimated_profit"].sum()
orders_count = filtered["invoice_no"].nunique()
customers_count = filtered["customer_id"].nunique()
aov = revenue / max(orders_count, 1)
clv = filtered.groupby("customer_id")["revenue"].sum().mean()
repeat_rate = customer_orders.gt(1).mean() * 100 if len(customer_orders) else 0

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Revenue", money(revenue))
k2.metric("Est. Profit", money(estimated_profit))
k3.metric("Orders", f"{orders_count:,}")
k4.metric("Customers", f"{customers_count:,}")
k5.metric("AOV", money(aov))
k6.metric("Repeat Rate", f"{repeat_rate:.1f}%")

tab_overview, tab_customers, tab_products, tab_sql = st.tabs(
    ["Executive Overview", "Customer Segments", "Product Mix", "SQL Evidence"]
)

with tab_overview:
    monthly = filtered.groupby("invoice_month", as_index=False)[["revenue", "estimated_profit"]].sum()
    left, right = st.columns(2)
    with left:
        st.subheader("Revenue and Estimated Profit Trend")
        st.line_chart(monthly, x="invoice_month", y=["revenue", "estimated_profit"], height=320)
    with right:
        st.subheader("Top Countries by Revenue")
        country = filtered.groupby("country", as_index=False)["revenue"].sum().nlargest(10, "revenue")
        bar_chart(country, "country", "revenue", "Revenue by Country")

with tab_customers:
    segments = customer_segments(filtered)
    left, right = st.columns([0.42, 0.58])
    with left:
        st.subheader("RFM Customer Segments")
        seg_summary = segments.groupby(["value_segment", "retention_segment"], observed=True).agg(
            customers=("customer_id", "count"),
            revenue=("monetary", "sum"),
            estimated_profit=("estimated_profit", "sum"),
        ).reset_index()
        st.dataframe(seg_summary, width="stretch", hide_index=True)
    with right:
        st.subheader("Top Customers by Lifetime Value")
        top = segments.sort_values("monetary", ascending=False).head(20)
        st.dataframe(top, width="stretch", hide_index=True)

with tab_products:
    st.subheader("Category Performance")
    category = filtered.groupby("product_category", as_index=False).agg(
        revenue=("revenue", "sum"),
        estimated_profit=("estimated_profit", "sum"),
        units=("quantity", "sum"),
        orders=("invoice_no", "nunique"),
    ).sort_values("revenue", ascending=False)
    st.dataframe(category, width="stretch", hide_index=True)

    st.subheader("Top Products")
    products = filtered.groupby(["stock_code", "description"], as_index=False).agg(
        revenue=("revenue", "sum"),
        units=("quantity", "sum"),
        customers=("customer_id", "nunique"),
    ).sort_values("revenue", ascending=False).head(25)
    st.dataframe(products, width="stretch", hide_index=True)

with tab_sql:
    st.subheader("SQL KPI Queries")
    st.code(Path("sql/business_kpis.sql").read_text(encoding="utf-8"), language="sql")
    st.subheader("Top CLV Customers from SQLite")
    top_sql = pd.read_sql_query(
        """
        SELECT customer_id,
               ROUND(SUM(revenue), 2) AS customer_lifetime_value,
               COUNT(DISTINCT invoice_no) AS orders,
               MAX(country) AS country
        FROM orders
        GROUP BY customer_id
        ORDER BY customer_lifetime_value DESC
        LIMIT 15
        """,
        conn,
    )
    st.dataframe(top_sql, width="stretch", hide_index=True)
