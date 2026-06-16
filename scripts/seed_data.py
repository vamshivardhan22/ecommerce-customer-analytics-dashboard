from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "ecommerce_orders.csv"


def build_sample(seed=42, rows=5000):
    rng = np.random.default_rng(seed)
    categories = ["Home Decor", "Stationery", "Kitchen", "Accessories", "Gifts & Toys", "General Merchandise"]
    countries = ["United Kingdom", "Germany", "France", "Netherlands", "Spain"]
    margins = {
        "Accessories": 0.32,
        "Home Decor": 0.28,
        "Stationery": 0.35,
        "Kitchen": 0.26,
        "Gifts & Toys": 0.30,
        "General Merchandise": 0.24,
    }
    records = []
    for i in range(rows):
        category = rng.choice(categories)
        quantity = int(rng.integers(1, 16))
        unit_price = round(float(rng.gamma(2.4, 3.2)), 2)
        revenue = round(quantity * unit_price, 2)
        records.append(
            {
                "invoice_no": f"INV-{rng.integers(10000, 99999)}",
                "stock_code": f"SKU-{rng.integers(1000, 9999)}",
                "description": f"{category} product",
                "quantity": quantity,
                "invoice_date": pd.Timestamp("2011-01-01") + pd.Timedelta(days=int(rng.integers(0, 335))),
                "unit_price": unit_price,
                "customer_id": str(int(rng.integers(12000, 19000))),
                "country": rng.choice(countries),
                "revenue": revenue,
                "estimated_profit": round(revenue * margins[category], 2),
                "product_category": category,
            }
        )
    return pd.DataFrame(records)


def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    build_sample().to_csv(OUTPUT, index=False)
    print(f"Wrote fallback ecommerce sample to {OUTPUT}")


if __name__ == "__main__":
    main()
