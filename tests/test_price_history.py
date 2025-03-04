import unittest
from decimal import Decimal

from fintual_stocks import PriceHistory


class TestPriceHistory(unittest.TestCase):
    def setUp(self):
        prices = {
            "2024-01-01": Decimal("150.0"),
            "2024-01-02": Decimal("152.0"),
            "2024-01-03": Decimal("155.0"),
            "2024-01-04": Decimal("157.0"),
        }
        self.price_history = PriceHistory(prices)

    def test_get_price(self):
        self.assertEqual(self.price_history.get_price("2024-01-01"), Decimal("150.0"))
        self.assertEqual(self.price_history.get_price("2024-01-04"), Decimal("157.0"))
        with self.assertRaises(ValueError):
            self.price_history.get_price("2024-01-05")

    def test_available_dates(self):
        self.assertCountEqual(
            self.price_history.available_dates(),
            ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
        )
