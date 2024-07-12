import logging
import os
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from jobs.models import Job, JobSkill, JobSearchTerm
from search_terms.models import SearchTerm
from services.job_readers.upwork_job_feed_reader import UpworkJobFeedReader
from skills.models import Skill


class Command(BaseCommand):
    help = 'Fetches job listings from Upwork RSS feed'

    def handle(self, *args, **kwargs):
        # Set up logging
        log_dir = settings.BASE_DIR / 'logs'
        os.makedirs(log_dir, exist_ok=True)
        log_filename = log_dir / f'fetch_upwork_jobs_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )
        logger = logging.getLogger(__name__)

        logger.info('Starting to fetch job listings from Upwork RSS feed')

        for search_term in SearchTerm.objects.all():
            url = settings.UPWORK_RSS_FEED_URL_T.format(page=1, search_term=search_term.encoded_text)

            for _job in UpworkJobFeedReader(url, 1, 1).fetch_jobs():
                job, created = Job.objects.get_or_create(
                    job_id=_job.job_id,
                    defaults={
                        'url': _job.url,
                        'published_date': _job.published_date,
                        'description': _job.description
                    }
                )

                JobSearchTerm.objects.get_or_create(job=job, search_term=search_term)

                for _skill in _job.skills:
                    skill, _ = Skill.objects.get_or_create(
                        slug=slugify(_skill),
                        defaults={'name': _skill}
                    )

                    JobSkill.objects.get_or_create(job=job, skill=skill)

                logger.info(f'Successfully processed job: {job}')
                self.stdout.write(self.style.SUCCESS(f'Successfully processed job: {job}'))

        logger.info('Successfully executed the command job: fetch_upwork_jobs')
        self.stdout.write(self.style.SUCCESS(f'Successfully executed the command job: fetch_upwork_jobs'))
