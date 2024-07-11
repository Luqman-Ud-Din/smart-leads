from django.urls import path

from job_reports.api.v1.jobs_published_by_search_terms_per_hour import JobsPublishedBySearchTermsPerHourAPIView, \
    JobsPublishedBySearchTermsPerHourCSVAPIView
from job_reports.api.v1.jobs_published_by_skills_per_hour import JobsPublishedBySkillsPerHourAPIView, \
    JobsPublishedBySkillsPerHourCSVAPIView
from job_reports.api.v1.jobs_published_per_hour import JobsPublishedPerHourAPIView, JobsPublishedPerHourCSVAPIView

API_V1 = 'v1'

urlpatterns = [
    path(
        f'jobs-published-by-search-terms-per-hour/',
        JobsPublishedBySearchTermsPerHourAPIView.as_view(),
        name=f'jobs-published-by-search-terms-per-hour-{API_V1}'
    ),
    path(
        f'jobs-published-by-search-terms-per-hour-csv/',
        JobsPublishedBySearchTermsPerHourCSVAPIView.as_view(),
        name=f'jobs-published-by-search-terms-per-hour-csv-{API_V1}'
    ),
    path(
        f'jobs-published-by-skills-per-hour/',
        JobsPublishedBySkillsPerHourAPIView.as_view(),
        name=f'jobs-published-by-skills-per-hour-{API_V1}'
    ),
    path(
        f'jobs-published-by-skills-per-hour-csv/',
        JobsPublishedBySkillsPerHourCSVAPIView.as_view(),
        name=f'jobs-published-by-skills-per-hour-csv-{API_V1}'
    ),
    path(
        f'jobs-published-per-hour/',
        JobsPublishedPerHourAPIView.as_view(),
        name=f'jobs-published-per-hour-{API_V1}'
    ),
    path(
        f'jobs-published-per-hour-csv/',
        JobsPublishedPerHourCSVAPIView.as_view(),
        name=f'jobs-published-per-hour-csv-{API_V1}'
    ),
]
