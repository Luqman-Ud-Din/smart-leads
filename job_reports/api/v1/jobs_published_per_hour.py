import csv

from django.conf import settings
from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from job_reports.serializers import DailyJobCountSerializer
from job_reports.utils import parse_dates, get_jobs_published_per_hour, start_date_query_param, end_date_query_param


class JobsPublishedPerHourAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            start_date_query_param,
            end_date_query_param
        ],
        responses={200: DailyJobCountSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        start_date, end_date, error_response = parse_dates(request, settings.REPORTS_CONFIGURATIONS['TO_TZ'])
        if error_response:
            return error_response

        data = get_jobs_published_per_hour(start_date, end_date)
        serializer = DailyJobCountSerializer(data, many=True)
        return Response(serializer.data)


class JobsPublishedPerHourCSVAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            start_date_query_param,
            end_date_query_param
        ],
        responses={200: 'CSV file with job counts by hour per day'}
    )
    def get(self, request, *args, **kwargs):
        start_date, end_date, error_response = parse_dates(request, settings.REPORTS_CONFIGURATIONS['TO_TZ'])
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
