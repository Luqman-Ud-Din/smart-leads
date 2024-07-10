from django.urls import path

from .api import (
    JobsCountByHourView, JobsCountByHourCSVView, JobsCountBySkillPerHourView,
    JobsCountBySkillPerHourCSVView, JobsPublishedPerHourView, JobsPublishedPerHourCSVView
)

urlpatterns = [
    path(
        'jobs-count-by-hour/',
        JobsCountByHourView.as_view(),
        name='jobs-count-by-hour'
    ),
    path(
        'jobs-count-by-hour-csv/',
        JobsCountByHourCSVView.as_view(),
        name='jobs-count-by-hour-csv'
    ),
    path(
        'jobs-count-by-skill-per-hour/',
        JobsCountBySkillPerHourView.as_view(),
        name='jobs-count-by-skill-per-hour'
    ),
    path(
        'jobs-count-by-skill-per-hour-csv/',
        JobsCountBySkillPerHourCSVView.as_view(),
        name='jobs-count-by-skill-per-hour-csv'
    ),
    path(
        'jobs-published-per-hour/',
        JobsPublishedPerHourView.as_view(),
        name='jobs-published-per-hour'
    ),
    path(
        'jobs-published-per-hour-csv/',
        JobsPublishedPerHourCSVView.as_view(),
        name='jobs-published-per-hour-csv'
    ),
]
