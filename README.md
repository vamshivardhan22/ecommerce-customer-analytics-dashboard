# E-Commerce Customer Analytics Dashboard

A Streamlit dashboard for analyzing online retail transactions and presenting sales, customer, product, and geography metrics. The project combines Python data preparation with KPI reporting and SQL queries used to validate business metrics.

## Features

- Revenue, order count, customer count, average order value, and repeat-purchase metrics.
- Estimated profit with transparent category-level margin assumptions.
- RFM-style customer segmentation and recency-based retention-risk bands.
- Product, country, and category performance views.
- SQL KPI queries for validating dashboard calculations.
- Cleaned transaction data included in the repository.

## Dataset

The project uses the Online Retail dataset from the UCI Machine Learning Repository. The data includes invoice identifiers, product codes and descriptions, quantities, invoice dates, unit prices, customer IDs, and countries.

The original data does not include cost of goods sold. As a result, profit is labeled **estimated profit** and relies on explicit category-level margin assumptions; it should not be interpreted as audited financial profit.

## Tech stack

- Python
- pandas
- Streamlit
- SQL

## Run locally

Requirements: Python and pip.

```bash
git clone https://github.com/vamshivardhan22/ecommerce-customer-analytics-dashboard.git
cd ecommerce-customer-analytics-dashboard
pip install -r requirements.txt
streamlit run app.py
```

Streamlit prints the local URL after the application starts.

## Project files

- `app.py` — dashboard interface and analytics.
- `data/ecommerce_orders.csv` — cleaned retail transaction data.
- `sql/business_kpis.sql` — SQL KPI validation queries.
- `scripts/seed_data.py` — synthetic data generator for reproducibility.

## Example questions

- Which customers contribute most to sales?
- Which customers have not purchased recently?
- Which products and countries generate the most revenue?
- What proportion of customers make repeat purchases?

## Skills demonstrated

Python, pandas, data cleaning, exploratory data analysis, KPI design, SQL analysis, customer segmentation, and dashboard development.
