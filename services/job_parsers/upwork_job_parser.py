import hashlib
import re
from datetime import datetime

from services.budget_parsers.budget_parser import BudgetParser
from services.job_container import JobContainer


class UpworkJobParser:
    def __init__(self, entry):
        self.entry = entry
        self.budget_parser = BudgetParser()

    def parse(self) -> JobContainer:
        published_date = self.parse_published_date()
        skills = self.parse_skills()
        url = self.parse_url()
        job_id = self.parse_job_id()
        description = self.parse_description()
        budget_info = self.budget_parser.parse_budget(self.entry.summary)

        return JobContainer(
            url=url,
            skills=skills,
            published_date=published_date,
            job_id=job_id,
            description=description,
            budget_info=budget_info,
        )

    def parse_published_date(self):
        return datetime.strptime(self.entry.published, '%a, %d %b %Y %H:%M:%S %z')

    def parse_skills(self):
        raw_skills = re.findall(r'<b>Skills</b>:(.*?)<br />', self.entry.summary, re.I)
        raw_skills = raw_skills[0] if len(raw_skills) > 0 else ''
        return set(skill.strip().lower() for skill in raw_skills.split(',') if skill.strip())

    def parse_url(self):
        return self.entry.link

    def parse_job_id(self):
        return hashlib.md5(str(self.entry.id).encode()).hexdigest()

    def parse_description(self):
        return (self.entry.summary or '').strip()
