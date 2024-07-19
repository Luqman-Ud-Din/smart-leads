import logging
import os
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from jobs.models import Job
from services.budget_parsers.budget_parser import BudgetParser


class Command(BaseCommand):
    help = 'Updates existing job listings with budget information'

    def handle(self, *args, **kwargs):
        # Set up logging
        log_dir = settings.BASE_DIR / 'logs'
        os.makedirs(log_dir, exist_ok=True)
        log_filename = log_dir / f'update_jobs_budget_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
        )
        logger = logging.getLogger(__name__)

        logger.info('Starting to update existing job listings with budget information')

        jobs = Job.objects.all()
        budget_parser = BudgetParser()
        jobs_to_update = []

        for job in jobs:
            budget_info = budget_parser.parse_budget(job.description)

            if budget_info:
                job.budget_type = budget_info.type
                job.budget_amount = budget_info.mean_amount
                job.budget_min_rate = budget_info.min_rate
                job.budget_max_rate = budget_info.max_rate
                jobs_to_update.append(job)

                logger.info(f'Prepared job for update: {job}')
                self.stdout.write(self.style.SUCCESS(f'Prepared job for update: {job}'))
            else:
                logger.info(f'No budget information found for job: {job}')
                self.stdout.write(self.style.WARNING(f'No budget information found for job: {job}'))

        if jobs_to_update:
            with transaction.atomic():
                Job.objects.bulk_update(
                    jobs_to_update,
                    ['budget_type', 'budget_amount', 'budget_min_rate', 'budget_max_rate']
                )

        logger.info('Successfully updated all existing job listings with budget information')
        self.stdout.write(self.style.SUCCESS(f'Successfully updated all existing job listings with budget information'))
