import csv

from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from job_reports.serializers import HourlyJobSkillCountSerializer
from job_reports.utils import parse_dates, get_jobs_published_by_skills_per_hour, start_date_query_param, \
    end_date_query_param


class JobsPublishedBySkillsPerHourAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            start_date_query_param,
            end_date_query_param
        ],
        responses={200: HourlyJobSkillCountSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        start_date, end_date, error_response = parse_dates(request)
        if error_response:
            return error_response

        data = get_jobs_published_by_skills_per_hour(start_date, end_date)
        serializer = HourlyJobSkillCountSerializer(data, many=True)
        return Response(serializer.data)


class JobsPublishedBySkillsPerHourCSVAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            start_date_query_param,
            end_date_query_param
        ],
        responses={200: 'CSV file with job counts by skill per hour'}
    )
    def get(self, request, *args, **kwargs):
        start_date, end_date, error_response = parse_dates(request)
        if error_response:
            return error_response

        data = get_jobs_published_by_skills_per_hour(start_date, end_date)

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
