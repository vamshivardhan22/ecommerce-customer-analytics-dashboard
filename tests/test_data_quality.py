import unittest
from pathlib import Path

import pandas as pd


class EcommerceDataQualityTests(unittest.TestCase):
    def setUp(self):
        self.data = pd.read_csv(Path("data/ecommerce_orders.csv"))

    def test_required_columns_exist(self):
        required = {
            "invoice_no",
            "stock_code",
            "description",
            "quantity",
            "invoice_date",
            "unit_price",
            "customer_id",
            "country",
            "revenue",
            "estimated_profit",
            "product_category",
        }
        self.assertTrue(required.issubset(self.data.columns))

    def test_revenue_and_customers_are_valid(self):
        self.assertGreater(len(self.data), 100000)
        self.assertGreater(self.data["revenue"].sum(), 1_000_000)
        self.assertGreater(self.data["customer_id"].nunique(), 1000)
        self.assertTrue((self.data["quantity"] > 0).all())
        self.assertTrue((self.data["unit_price"] > 0).all())


if __name__ == "__main__":
    unittest.main()
