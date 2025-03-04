import unittest
from decimal import Decimal

from fintual_stocks import Portfolio, PriceHistory


class TestPortfolioIntegration(unittest.TestCase):
    def setUp(self):
        apple_prices = {
            "2019-01-01": Decimal("150.0"),
            "2020-01-01": Decimal("160.0"),
            "2021-01-01": Decimal("170.0"),
            "2022-01-01": Decimal("180.0"),
            "2023-01-01": Decimal("190.0"),
        }
        nvda_prices = {
            "2019-01-01": Decimal("100.0"),
            "2020-01-01": Decimal("110.0"),
            "2021-01-01": Decimal("120.0"),
            "2022-01-01": Decimal("130.0"),
            "2023-01-01": Decimal("140.0"),
        }
        apple_price_history = PriceHistory(apple_prices)
        nvda_price_history = PriceHistory(nvda_prices)

        self.portfolio = Portfolio()
        self.portfolio.add_stock("AAPL", apple_price_history)
        self.portfolio.add_stock("NVDA", nvda_price_history)

        # Transactions for AAPL:
        # 2019-01-01: Buy 10 shares
        # 2021-01-01: Buy 5 shares
        # 2022-01-01: Sell 2 shares
        self.portfolio.add_transaction("AAPL", "2019-01-01", Decimal("10"))
        self.portfolio.add_transaction("AAPL", "2021-01-01", Decimal("5"))
        self.portfolio.add_transaction("AAPL", "2022-01-01", Decimal("-2"))

        # Transactions for NVDA:
        # 2019-01-01: Buy 20 shares
        # 2020-01-01: Buy 10 shares
        # 2023-01-01: Sell 5 shares
        self.portfolio.add_transaction("NVDA", "2019-01-01", Decimal("20"))
        self.portfolio.add_transaction("NVDA", "2020-01-01", Decimal("10"))
        self.portfolio.add_transaction("NVDA", "2023-01-01", Decimal("-5"))

    def test_portfolio_value(self):
        # 2019-01-01:
        # AAPL: 10 * 150 = 1500; NVDA: 20 * 100 = 2000; Total = 3500.
        self.assertEqual(
            self.portfolio.portfolio_value("2019-01-01"), Decimal("3500.0")
        )
        # 2023-01-01:
        # AAPL effective shares = 10 + 5 - 2 = 13; Value = 13 * 190 = 2470.
        # NVDA effective shares = 20 + 10 - 5 = 25; Value = 25 * 140 = 3500.
        # Total = 2470 + 3500 = 5970.
        self.assertEqual(
            self.portfolio.portfolio_value("2023-01-01"), Decimal("5970.0")
        )

    def test_profit(self):
        # Profit from 2019-01-01 to 2023-01-01 = 5970 - 3500 = 2470.
        self.assertEqual(
            self.portfolio.profit("2019-01-01", "2023-01-01"), Decimal("2470.0")
        )

    def test_annualized_return(self):
        # 2019-01-01 to 2023-01-01 (4 years):
        # Start value: AAPL = 10*150=1500, NVDA = 20*100=2000, total = 3500.
        # End value: AAPL = 13*190=2470, NVDA = 25*140=3500, total = 5970.
        # annualized_return = (5970/3500)^(1/4) - 1.
        ratio = 5970 / 3500
        expected_return = ratio ** (1 / 4) - 1
        ret = self.portfolio.annualized_return("2019-01-01", "2023-01-01")
        self.assertAlmostEqual(ret, expected_return, places=2)
