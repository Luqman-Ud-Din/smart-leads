from datetime import datetime, timedelta

from drf_yasg import openapi
from rest_framework import status
from rest_framework.response import Response

from jobs.models import JobSearchTerm, JobSkill, Job
from search_terms.models import SearchTerm
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
            jobs_count = JobSearchTerm.objects.filter(
                search_term=search_term,
                job__published_date__date__range=(start_date, end_date),
                job__published_date__hour=hour
            ).count()

            hourly_data['job_counts'].append({
                'search_term': search_term.text,
                'jobs_count': jobs_count
            })

        data.append(hourly_data)

    return data


def get_jobs_published_by_skills_per_hour(start_date, end_date):
    data = []

    for hour in range(24):
        hourly_data = {'hour': hour, 'job_counts': []}

        for skill in Skill.objects.all():
            jobs_count = JobSkill.objects.filter(
                skill=skill,
                job__published_date__date__range=(start_date, end_date),
                job__published_date__hour=hour
            ).count()

            hourly_data['job_counts'].append({
                'skill': skill.name,
                'jobs_count': jobs_count
            })

        data.append(hourly_data)

    return data


def get_jobs_published_per_hour(start_date, end_date):
    data = []

    current_date = start_date
    while current_date <= end_date:
        daily_data = {'date': current_date.strftime('%Y-%m-%d'), 'job_counts': []}
        for hour in range(24):
            jobs_count = Job.objects.filter(
                published_date__date=current_date,
                published_date__hour=hour
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
