import csv

from django.http import HttpResponse
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import HourlyJobCountSerializer, HourlyJobSkillCountSerializer, DailyJobCountSerializer
from .utils import get_jobs_count_by_hour, parse_dates, get_jobs_count_by_skill_per_hour, get_jobs_published_per_hour


class JobsCountByHourView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: HourlyJobCountSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        start_date, end_date, error_response = parse_dates(request)
        if error_response:
            return error_response

        data = get_jobs_count_by_hour(start_date, end_date)
        serializer = HourlyJobCountSerializer(data, many=True)
        return Response(serializer.data)


class JobsCountByHourCSVView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: 'CSV file with job counts by hour'}
    )
    def get(self, request, *args, **kwargs):
        start_date, end_date, error_response = parse_dates(request)
        if error_response:
            return error_response

        data = get_jobs_count_by_hour(start_date, end_date)

        # Initialize CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="jobs_count_by_hour.csv"'

        writer = csv.writer(response)
        header = ['search_term'] + [str(hour) for hour in range(24)]
        writer.writerow(header)

        search_term_counts = {}
        for item in data:
            for job_count in item['job_counts']:
                search_term = job_count['search_term']
                if search_term not in search_term_counts:
                    search_term_counts[search_term] = [0] * 24
                search_term_counts[search_term][item['hour']] = job_count['jobs_count']

        for search_term, counts in search_term_counts.items():
            row = [search_term] + counts
            writer.writerow(row)

        return response


class JobsCountBySkillPerHourView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: HourlyJobSkillCountSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        start_date, end_date, error_response = parse_dates(request)
        if error_response:
            return error_response

        data = get_jobs_count_by_skill_per_hour(start_date, end_date)
        serializer = HourlyJobSkillCountSerializer(data, many=True)
        return Response(serializer.data)


class JobsCountBySkillPerHourCSVView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: 'CSV file with job counts by skill per hour'}
    )
    def get(self, request, *args, **kwargs):
        start_date, end_date, error_response = parse_dates(request)
        if error_response:
            return error_response

        data = get_jobs_count_by_skill_per_hour(start_date, end_date)

        # Initialize CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="jobs_count_by_skill_per_hour.csv"'

        writer = csv.writer(response)
        header = ['skill'] + [str(hour) for hour in range(24)]
        writer.writerow(header)

        skill_counts = {}
        for item in data:
            for job_count in item['job_counts']:
                skill = job_count['skill']
                if skill not in skill_counts:
                    skill_counts[skill] = [0] * 24
                skill_counts[skill][item['hour']] = job_count['jobs_count']

        for skill, counts in skill_counts.items():
            row = [skill] + counts
            writer.writerow(row)

        return response


class JobsPublishedPerHourView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: DailyJobCountSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        start_date, end_date, error_response = parse_dates(request)
        if error_response:
            return error_response

        data = get_jobs_published_per_hour(start_date, end_date)
        serializer = DailyJobCountSerializer(data, many=True)
        return Response(serializer.data)


class JobsPublishedPerHourCSVView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date', openapi.IN_QUERY,
                description="Start date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'end_date', openapi.IN_QUERY,
                description="End date (YYYY-MM-DD)",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: 'CSV file with job counts by hour per day'}
    )
    def get(self, request, *args, **kwargs):
        start_date, end_date, error_response = parse_dates(request)
        if error_response:
            return error_response

        data = get_jobs_published_per_hour(start_date, end_date)

        # Initialize CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="jobs_published_per_hour.csv"'

        writer = csv.writer(response)
        header = ['date'] + [str(hour) for hour in range(24)]
        writer.writerow(header)

        for daily_data in data:
            row = [daily_data['date']] + daily_data['job_counts']
            writer.writerow(row)

        return response
