from dataclasses import dataclass
from datetime import datetime
from typing import Set, Dict, Optional

from services.budget_container import BudgetContainer


@dataclass
class JobContainer:
    job_id: str
    url: str
    description: str
    skills: Set[str]
    published_date: datetime
    budget_info: Optional[BudgetContainer] = None

    def to_dict(self) -> Dict:
        return {
            'job_id': self.job_id,
            'url': self.url,
            'description': self.description,
            'skills': self.skills,
            'published_date': self.published_date,
            'budget_info': self.budget_info.to_dict() if self.budget_info else None,
        }
