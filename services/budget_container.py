from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class BudgetContainer:
    type: str
    amount: Optional[float] = None
    min_rate: Optional[float] = None
    max_rate: Optional[float] = None

    @property
    def mean_amount(self) -> Optional[float]:
        if self.min_rate is not None and self.max_rate is not None:
            return (self.min_rate + self.max_rate) / 2
        return self.amount

    def to_dict(self) -> Dict:
        return {
            'type': self.type,
            'amount': self.mean_amount,
            'min_rate': self.min_rate,
            'max_rate': self.max_rate
        }
