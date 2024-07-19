import re
from typing import Optional

from services.budget_container import BudgetContainer


class BudgetParser:
    FIXED_BUDGET_PATTERN = re.compile(
        r'<b>\s*Budget\s*</b>\s*:\s*\$([\d,]+(?:\.\d{2})?)',
        re.I | re.DOTALL
    )
    HOURLY_RANGE_PATTERN = re.compile(
        r'<b>\s*Hourly\s+Range\s*</b>\s*:\s*\$([\d,]+(?:\.\d{2})?)\s*-\s*\$([\d,]+(?:\.\d{2})?)',
        re.I | re.DOTALL
    )
    HOURLY_RATE_PATTERN = re.compile(
        r'<b>\s*Hourly\s+Rate\s*</b>\s*:\s*\$([\d,]+(?:\.\d{2})?)',
        re.I | re.DOTALL
    )

    def parse_budget(self, summary: str) -> Optional[BudgetContainer]:
        return (
                self.parse_fixed_budget(summary) or
                self.parse_hourly_range(summary) or
                self.parse_hourly_rate(summary)
        )

    def parse_fixed_budget(self, summary: str) -> Optional[BudgetContainer]:
        match = self.FIXED_BUDGET_PATTERN.search(summary)
        if not match:
            return

        amount = self.sanitize_amount(match.group(1))
        return BudgetContainer(type='fixed', amount=amount)

    def parse_hourly_range(self, summary: str) -> Optional[BudgetContainer]:
        match = self.HOURLY_RANGE_PATTERN.search(summary)
        if not match:
            return

        min_rate = self.sanitize_amount(match.group(1))
        max_rate = self.sanitize_amount(match.group(2))
        return BudgetContainer(
            type='hourly_range',
            min_rate=min_rate,
            max_rate=max_rate
        )

    def parse_hourly_rate(self, summary: str) -> Optional[BudgetContainer]:
        match = self.HOURLY_RATE_PATTERN.search(summary)
        if not match:
            return

        amount = self.sanitize_amount(match.group(1))
        return BudgetContainer(type='hourly', amount=amount)

    def sanitize_amount(self, value: str) -> float:
        """Sanitize the monetary value by removing commas and converting to float."""
        return float(value.replace(',', ''))
