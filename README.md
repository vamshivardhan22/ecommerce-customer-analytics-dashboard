# E-Commerce Customer Analytics Dashboard

A CEO-ready ecommerce analytics dashboard built with a real public retail dataset. The project turns raw transaction data into executive KPIs, customer segmentation, product insights, and SQL-backed analysis.

## Dataset

Source: UCI Machine Learning Repository, **Online Retail** dataset.

The dataset contains UK-based online retail transactions with invoice number, stock code, product description, quantity, invoice date, unit price, customer ID, and country.

Important note: the dataset does not include cost of goods sold. The dashboard therefore labels profit as **Estimated Profit**, calculated with transparent category-level margin assumptions.

## Features

- Revenue, estimated profit, order count, customer count, AOV, CLV, and repeat purchase rate.
- RFM-style customer segmentation.
- Retention risk bands based on recency.
- Country, category, and product performance.
- SQL evidence queries for KPI validation.
- Cleaned dataset included at `data/ecommerce_orders.csv`.

## Run Locally

```powershell
pip install -r requirements.txt
streamlit run app.py
```

## Portfolio Story

This dashboard answers boardroom-style questions:

- Which customers are most valuable?
- Which customers are at risk of going dormant?
- Which countries and product categories drive revenue?
- What is the repeat purchase profile of the customer base?
- Where should leadership focus retention and merchandising efforts?

## Project Files

- `app.py` - Streamlit executive dashboard.
- `data/ecommerce_orders.csv` - cleaned real retail transaction data.
- `sql/business_kpis.sql` - SQL KPI validation queries.
- `scripts/seed_data.py` - fallback synthetic generator kept for reproducibility.

