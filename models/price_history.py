from dataclasses import dataclass
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
