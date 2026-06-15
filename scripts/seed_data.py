from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT = DATA_DIR / "ecommerce_orders.csv"


def build_orders(seed=42, rows=6000):
    rng = np.random.default_rng(seed)
    DATA_DIR.mkdir(exist_ok=True)

    customers = [f"CUST-{i:05d}" for i in range(1, 1201)]
    segments = ["Consumer", "Corporate", "Home Office"]
    regions = ["North", "South", "East", "West", "Central"]
    categories = {
        "Technology": ["Phones", "Accessories", "Laptops", "Printers"],
        "Furniture": ["Chairs", "Tables", "Bookcases", "Storage"],
        "Office Supplies": ["Paper", "Binders", "Labels", "Art"],
    }

    records = []
    start = pd.Timestamp("2024-01-01")
    for i in range(rows):
        category = rng.choice(list(categories))
        sub_category = rng.choice(categories[category])
        sales = round(float(rng.gamma(shape=3.2, scale=85)), 2)
        discount = float(rng.choice([0, 0.05, 0.1, 0.15, 0.2, 0.3], p=[0.38, 0.18, 0.18, 0.12, 0.09, 0.05]))
        margin = {
            "Technology": rng.normal(0.22, 0.08),
            "Furniture": rng.normal(0.13, 0.12),
            "Office Supplies": rng.normal(0.18, 0.07),
        }[category]
        profit = round(sales * (margin - discount * 0.55), 2)
        records.append(
            {
                "order_id": f"ORD-{i + 1:06d}",
                "order_date": start + pd.Timedelta(days=int(rng.integers(0, 730))),
                "customer_id": rng.choice(customers),
                "segment": rng.choice(segments, p=[0.56, 0.29, 0.15]),
                "region": rng.choice(regions),
                "category": category,
                "sub_category": sub_category,
                "product_id": f"SKU-{category[:3].upper()}-{rng.integers(100, 999)}",
                "quantity": int(rng.integers(1, 8)),
                "sales": sales,
                "discount": discount,
                "profit": profit,
                "shipping_cost": round(float(rng.uniform(4, 45)), 2),
            }
        )

    orders = pd.DataFrame(records)
    orders["order_date"] = pd.to_datetime(orders["order_date"]).dt.date
    return orders.sort_values("order_date")


def main():
    orders = build_orders()
    orders.to_csv(OUTPUT, index=False)
    print(f"Wrote {len(orders):,} ecommerce orders to {OUTPUT}")


if __name__ == "__main__":
    main()
