from datetime import datetime
from datetime import timedelta

from django.conf import settings
from django.db.models import F, Count
from django.db.models.functions import TruncHour
from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response

from jobs.models import JobSearchTerm, JobSkill, Job
from search_terms.models import SearchTerm
from services.db.functions import ConvertTimeZone
from skills.models import Skill


def parse_dates(request):
    start_date_str = request.query_params.get('start_date')
    end_date_str = request.query_params.get('end_date')

    try:
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        else:
            start_date = datetime.now().date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        else:
            end_date = datetime.now().date()

    except ValueError:
        return None, None, Response({'error': 'Invalid date format. Use YYYY-MM-DD.'},
                                    status=status.HTTP_400_BAD_REQUEST)

    return start_date, end_date, None


def get_jobs_published_by_search_terms_per_hour(start_date, end_date):
    data = []

    for hour in range(24):
        hourly_data = {'hour': hour, 'job_counts': []}

        for search_term in SearchTerm.objects.all():
            jobs_count = JobSearchTerm.objects.annotate(
                local_published_date=ConvertTimeZone(
                    F('job__published_date'),
                    settings.REPORTS_CONFIGURATIONS['DB_FROM_TZ'],
                    settings.REPORTS_CONFIGURATIONS['DB_TO_TZ']
                )
            ).filter(
                search_term=search_term,
                local_published_date__date__range=(start_date, end_date),
                local_published_date__hour=hour
            ).count()

            hourly_data['job_counts'].append({
                'search_term': search_term.text,
                'jobs_count': jobs_count
            })

        data.append(hourly_data)

    return data


def get_jobs_published_by_skills_per_hour(start_date, end_date):
    all_skills = Skill.objects.order_by('name').values_list('name', flat=True)

    annotated_jobs = JobSkill.objects.annotate(
        local_published_date=ConvertTimeZone(
            F('job__published_date'),
            settings.REPORTS_CONFIGURATIONS['DB_FROM_TZ'],
            settings.REPORTS_CONFIGURATIONS['DB_TO_TZ']
        )
    ).filter(
        local_published_date__date__range=(start_date, end_date)
    ).annotate(
        hour=TruncHour('local_published_date')
    ).values(
        'hour', 'skill__name'
    ).annotate(
        jobs_count=Count('id')
    ).order_by('hour', 'skill__name')

    data = [
        {
            'hour': hour,
            'job_counts': [
                {'skill': skill, 'jobs_count': 0}
                for skill in all_skills
            ]
        } for hour in range(24)
    ]

    for entry in annotated_jobs:
        hour = entry['hour'].hour
        skill_name = entry['skill__name']
        jobs_count = entry['jobs_count']

        for job_count in data[hour]['job_counts']:
            if job_count['skill'] == skill_name:
                job_count['jobs_count'] = jobs_count
                break

    return data


def get_jobs_published_per_hour(start_date, end_date):
    data = []

    current_date = start_date
    while current_date <= end_date:
        daily_data = {'date': current_date.strftime('%Y-%m-%d'), 'job_counts': []}
        for hour in range(24):
            jobs_count = Job.objects.annotate(
                local_published_date=ConvertTimeZone(
                    F('published_date'),
                    settings.REPORTS_CONFIGURATIONS['DB_FROM_TZ'],
                    settings.REPORTS_CONFIGURATIONS['DB_TO_TZ']
                )
            ).filter(
                local_published_date__date=current_date,
                local_published_date__hour=hour
            ).count()
            daily_data['job_counts'].append(jobs_count)
        data.append(daily_data)
        current_date += timedelta(days=1)

    return data


start_date_query_param = openapi.Parameter(
    'start_date', openapi.IN_QUERY,
    description="Start date (YYYY-MM-DD)",
    type=openapi.TYPE_STRING
)

end_date_query_param = openapi.Parameter(
    'end_date', openapi.IN_QUERY,
    description="End date (YYYY-MM-DD)",
    type=openapi.TYPE_STRING
)
