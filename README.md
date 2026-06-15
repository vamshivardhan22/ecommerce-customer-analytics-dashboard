# E-Commerce Customer Analytics Dashboard

An executive analytics dashboard for ecommerce revenue, profit, customer value, and retention behavior. The project demonstrates SQL, Python, KPI design, dashboard storytelling, and Power BI-ready data exports.

## Highlights

- Revenue, profit, average order value, customer lifetime value, and repeat purchase rate.
- Customer segmentation using RFM-style value bands.
- Category, regional, and monthly performance views.
- SQLite-backed KPI queries in `sql/business_kpis.sql`.
- Streamlit dashboard designed for fast executive review.

## Run Locally

```powershell
pip install -r requirements.txt
python .\scripts\seed_data.py
streamlit run app.py
```

The app automatically creates `data/ecommerce_orders.csv` if it does not exist.

## Portfolio Story

This project answers CEO-style questions:

- Which customer groups generate the most value?
- Are revenue and profit moving together?
- Which regions and categories deserve investment?
- How strong is repeat purchase behavior?

## Power BI Extension

Import `data/ecommerce_orders.csv` into Power BI and recreate:

- KPI cards: revenue, profit, AOV, CLV, repeat purchase rate.
- Line chart: monthly revenue and profit.
- Bar charts: revenue by region/category.
- Table: top customers by CLV.

