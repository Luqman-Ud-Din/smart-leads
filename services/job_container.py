from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict


@dataclass
class JobContainer:
    job_id: str
    url: str
    skills: List[str]
    published_date: datetime

    def to_dict(self) -> Dict:
        return {
            'job_id': self.job_id,
            'url': self.url,
            'skills': self.skills,
            'published_date': self.published_date
        }
