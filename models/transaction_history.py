from bisect import bisect_right
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, Optional


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
