import unittest
from decimal import Decimal

from fintual_stocks import TransactionHistory


class TestTransactionHistory(unittest.TestCase):
    def setUp(self):
        self.transaction_history = TransactionHistory()
        self.transaction_history.add_transaction("2024-01-01", Decimal("10"))
        self.transaction_history.add_transaction("2024-01-02", Decimal("5"))
        self.transaction_history.add_transaction("2024-01-03", Decimal("-3"))

    def test_effective_shares_with_date(self):
        self.assertEqual(
            self.transaction_history.effective_shares("2024-01-02"), Decimal("15")
        )

    def test_effective_shares_without_date(self):
        self.assertEqual(self.transaction_history.effective_shares(), Decimal("12"))
