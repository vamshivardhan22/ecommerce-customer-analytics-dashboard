import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from scripts.seed_data import OUTPUT, main as seed_data


st.set_page_config(page_title="E-Commerce Analytics", layout="wide")


def ensure_data():
    if not OUTPUT.exists():
        seed_data()
    orders = pd.read_csv(OUTPUT, parse_dates=["order_date"])
    return orders


def money(value):
    return f"${value:,.0f}"


def build_connection(orders):
    conn = sqlite3.connect(":memory:")
    orders.to_sql("orders", conn, index=False, if_exists="replace")
    return conn


def customer_segments(orders):
    snapshot = orders["order_date"].max() + pd.Timedelta(days=1)
    rfm = orders.groupby("customer_id").agg(
        recency=("order_date", lambda x: (snapshot - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("sales", "sum"),
        profit=("profit", "sum"),
    )
    rfm["segment"] = pd.cut(
        rfm["monetary"],
        bins=[-1, 250, 700, 1400, float("inf")],
        labels=["Low Value", "Developing", "Loyal", "VIP"],
    )
    return rfm.reset_index()


def bar_chart(data, x, y, title):
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=data, x=x, y=y, ax=ax, palette="crest")
    ax.set_title(title)
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(rotation=20)
    st.pyplot(fig, clear_figure=True)


orders = ensure_data()
conn = build_connection(orders)
segments = customer_segments(orders)

st.title("E-Commerce Customer Analytics Dashboard")
st.caption("CEO-ready view of revenue, profit, customers, segments, and repeat purchase behavior.")

with st.sidebar:
    st.header("Filters")
    min_date, max_date = orders["order_date"].min(), orders["order_date"].max()
    date_range = st.date_input("Order date range", value=(min_date, max_date))
    selected_regions = st.multiselect("Region", sorted(orders["region"].unique()), default=sorted(orders["region"].unique()))
    selected_segments = st.multiselect("Customer segment", sorted(orders["segment"].unique()), default=sorted(orders["segment"].unique()))

filtered = orders[
    (orders["order_date"].dt.date >= date_range[0])
    & (orders["order_date"].dt.date <= date_range[1])
    & (orders["region"].isin(selected_regions))
    & (orders["segment"].isin(selected_segments))
]

repeat_customers = filtered.groupby("customer_id")["order_id"].nunique()
revenue = filtered["sales"].sum()
profit = filtered["profit"].sum()
aov = revenue / max(filtered["order_id"].nunique(), 1)
clv = filtered.groupby("customer_id")["sales"].sum().mean()
repeat_rate = (repeat_customers.gt(1).mean() * 100) if len(repeat_customers) else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Revenue", money(revenue))
k2.metric("Profit", money(profit))
k3.metric("Avg Order Value", money(aov))
k4.metric("Avg CLV", money(clv))
k5.metric("Repeat Rate", f"{repeat_rate:.1f}%")

tab_overview, tab_customers, tab_sql = st.tabs(["Executive Overview", "Customer Segments", "SQL Evidence"])

with tab_overview:
    left, right = st.columns(2)
    monthly = filtered.assign(month=filtered["order_date"].dt.to_period("M").astype(str)).groupby("month", as_index=False)[["sales", "profit"]].sum()
    with left:
        st.subheader("Revenue and Profit Trend")
        st.line_chart(monthly, x="month", y=["sales", "profit"], height=320)
    with right:
        st.subheader("Revenue by Category")
        category = filtered.groupby("category", as_index=False)["sales"].sum().sort_values("sales", ascending=False)
        bar_chart(category, "category", "sales", "Revenue by Category")

    region = filtered.groupby("region", as_index=False)[["sales", "profit"]].sum().sort_values("sales", ascending=False)
    st.subheader("Regional Performance")
    st.dataframe(region, use_container_width=True, hide_index=True)

with tab_customers:
    filtered_segments = customer_segments(filtered)
    c1, c2 = st.columns([0.45, 0.55])
    with c1:
        st.subheader("Customer Value Segmentation")
        seg_summary = filtered_segments.groupby("segment", observed=True).agg(
            customers=("customer_id", "count"),
            revenue=("monetary", "sum"),
            profit=("profit", "sum"),
        ).reset_index()
        st.dataframe(seg_summary, use_container_width=True, hide_index=True)
    with c2:
        st.subheader("Top Customers by Lifetime Value")
        top = filtered_segments.sort_values("monetary", ascending=False).head(15)
        st.dataframe(top, use_container_width=True, hide_index=True)

with tab_sql:
    st.subheader("SQL KPI Queries")
    st.code(Path("sql/business_kpis.sql").read_text(encoding="utf-8"), language="sql")
    st.subheader("Top Customer CLV from SQLite")
    top_sql = pd.read_sql_query(
        """
        SELECT customer_id, ROUND(SUM(sales), 2) AS clv, COUNT(DISTINCT order_id) AS orders
        FROM orders
        GROUP BY customer_id
        ORDER BY clv DESC
        LIMIT 10
        """,
        conn,
    )
    st.dataframe(top_sql, use_container_width=True, hide_index=True)
