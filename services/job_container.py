from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Set


@dataclass
class JobContainer:
    job_id: str
    url: str
    description: str
    skills: Set[str]
    published_date: datetime

    def to_dict(self) -> Dict:
        return {
            'job_id': self.job_id,
            'url': self.url,
            'description': self.description,
            'skills': self.skills,
            'published_date': self.published_date
        }
