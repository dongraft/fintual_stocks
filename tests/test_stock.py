import unittest
from decimal import Decimal

from fintual_stocks import Stock
from models import PriceHistory


class TestStock(unittest.TestCase):
    def setUp(self):
        self.prices = {
            "2024-01-01": Decimal("100.0"),
            "2024-01-02": Decimal("105.0"),
            "2024-01-03": Decimal("110.0"),
        }
        price_history = PriceHistory(self.prices)
        self.stock = Stock("NVDA", price_history)
        self.stock.add_transaction("2024-01-01", Decimal("20"))
        self.stock.add_transaction("2024-01-02", Decimal("5"))
        self.stock.add_transaction("2024-01-03", Decimal("-3"))

    def test_price(self):
        self.assertEqual(self.stock.price("2024-01-01"), Decimal("100.0"))
        self.assertEqual(self.stock.price("2024-01-03"), Decimal("110.0"))

    def test_effective_shares(self):
        self.assertEqual(self.stock.effective_shares("2024-01-03"), Decimal("22"))

    def test_value(self):
        self.assertEqual(self.stock.value("2024-01-03"), Decimal("2420"))
