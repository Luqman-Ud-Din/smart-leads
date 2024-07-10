from feedparser import FeedParserDict, parse

from services.job_parsers.upwork_job_parser import UpworkJobParser
from services.request_scheduler.request_scheduler import RequestScheduler


class UpworkJobFeedReader:
    def __init__(self, base_url, max_pages=50, max_workers=16):
        self.base_url = base_url
        self.max_pages = max_pages
        self.scheduler = RequestScheduler(max_workers=max_workers)

    def fetch_feed(self, page):
        feed_url = self.base_url.format(page=page)
        try:
            feed = parse(feed_url)
            return feed, page
        except Exception as e:
            return e, page

    def fetch_jobs(self):
        job_ids = set()
        tasks = [lambda page=page: self.fetch_feed(page) for page in range(self.max_pages + 1)]

        for feed, page in self.scheduler.execute_generator(tasks):
            if not isinstance(feed, FeedParserDict) or feed.status != 200:
                print(feed)
                continue

            for entry in feed.entries:
                parser = UpworkJobParser(entry)
                job = parser.parse()

                if job.job_id not in job_ids:
                    job_ids.add(job.job_id)
                    yield job
