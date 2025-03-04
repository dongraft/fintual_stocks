import time
from bisect import bisect_right
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List, Optional


@dataclass
class PriceHistory:
    prices: Dict[str, Decimal]

    def get_price(self, date: Optional[str] = None) -> Decimal:
        if date is None:
            date = max(self.prices.keys())
        if date not in self.prices:
            raise ValueError(f"Price for date {date} not found.")
        return self.prices[date]

    def available_dates(self) -> List[str]:
        return sorted(self.prices.keys())


@dataclass
class TransactionHistory:
    daily_accumulated: Dict[str, Decimal] = field(default_factory=dict)
    _last_total: Decimal = field(default=Decimal("0"), init=False)

    def add_transaction(self, date: str, amount: Decimal) -> None:
        self._last_total += amount
        self.daily_accumulated[date] = self._last_total

    def effective_shares(self, date: Optional[str] = None) -> Decimal:
        if not self.daily_accumulated:
            return Decimal("0")
        if date is None:
            return list(self.daily_accumulated.values())[-1]
        if date in self.daily_accumulated:
            return self.daily_accumulated[date]
        dates = sorted(self.daily_accumulated.keys())
        pos = bisect_right(dates, date)
        if pos == 0:
            raise ValueError(f"Date {date} not found.")
        return self.daily_accumulated[dates[pos - 1]]


class Stock:
    def __init__(self, ticker: str, price_history: PriceHistory):
        self.ticker = ticker
        self.price_history = price_history
        self.transaction_history = TransactionHistory()

    def price(self, date: Optional[str] = None) -> Decimal:
        return self.price_history.get_price(date)

    def effective_shares(self, date: Optional[str] = None) -> Decimal:
        return self.transaction_history.effective_shares(date)

    def value(self, date: Optional[str] = None) -> Decimal:
        effective_date = date or self.price_history.available_dates()[-1]
        return self.effective_shares(effective_date) * self.price(effective_date)

    def available_dates(self) -> List[str]:
        return sorted(self.price_history.available_dates())

    def add_transaction(self, date: str, amount: Decimal) -> None:
        self.transaction_history.add_transaction(date, amount)


class Portfolio:
    def __init__(self):
        self.stocks: Dict[str, Stock] = {}

    def add_stock(self, ticker: str, price_history: PriceHistory) -> None:
        if ticker in self.stocks:
            raise ValueError(f"Stock with ticker {ticker} already exists.")
        self.stocks[ticker] = Stock(ticker, price_history)

    def add_transaction(self, ticker: str, date: str, amount: Decimal) -> None:
        if ticker not in self.stocks:
            raise ValueError(f"Stock with ticker {ticker} not found.")
        self.stocks[ticker].add_transaction(date, amount)

    def portfolio_value(self, date: Optional[str] = None) -> Decimal:
        if not self.stocks:
            return Decimal("0")

        return sum((stock.value(date) for stock in self.stocks.values()), Decimal("0"))

    def profit(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> Decimal:
        sample_stock = next(iter(self.stocks.values()))
        all_dates = sample_stock.price_history.available_dates()
        effective_start = start_date or all_dates[0]
        effective_end = end_date or all_dates[-1]
        return self.portfolio_value(effective_end) - self.portfolio_value(
            effective_start
        )

    def annualized_return(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> float:
        sample_stock = next(iter(self.stocks.values()))
        all_dates = sample_stock.price_history.available_dates()
        effective_start = start_date or all_dates[0]
        effective_end = end_date or all_dates[-1]
        start_value = self.portfolio_value(effective_start)
        end_value = self.portfolio_value(effective_end)
        if start_value == Decimal("0"):
            raise ValueError("Start value is zero, cannot compute annualized return.")
        t1 = time.strptime(effective_start, "%Y-%m-%d")
        t2 = time.strptime(effective_end, "%Y-%m-%d")
        days = (time.mktime(t2) - time.mktime(t1)) / (24 * 3600)
        if days <= 0:
            raise ValueError("End date must be after start date.")
        years = days / 365.0
        return (float(end_value) / float(start_value)) ** (1 / years) - 1
