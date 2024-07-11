import csv

from django.http import HttpResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from job_reports.serializers import HourlyJobCountSerializer
from job_reports.utils import parse_dates, get_jobs_published_by_search_terms_per_hour, start_date_query_param, \
    end_date_query_param


class JobsPublishedBySearchTermsPerHourAPIView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            start_date_query_param,
            end_date_query_param
        ],
        responses={200: HourlyJobCountSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        start_date, end_date, error_response = parse_dates(request)
        if error_response:
            return error_response

        data = get_jobs_published_by_search_terms_per_hour(start_date, end_date)
        serializer = HourlyJobCountSerializer(data, many=True)
        return Response(serializer.data)


class JobsPublishedBySearchTermsPerHourCSVAPIView(APIView):
    @swagger_auto_schema(
        start_date_query_param,
        end_date_query_param,
        responses={200: 'CSV file with job counts by hour'}
    )
    def get(self, request, *args, **kwargs):
        start_date, end_date, error_response = parse_dates(request)
        if error_response:
            return error_response

        data = get_jobs_published_by_search_terms_per_hour(start_date, end_date)

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
