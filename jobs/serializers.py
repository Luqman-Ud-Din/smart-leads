from rest_framework import serializers


class JobCountSerializer(serializers.Serializer):
    search_term = serializers.CharField()
    jobs_count = serializers.IntegerField()


class HourlyJobCountSerializer(serializers.Serializer):
    hour = serializers.IntegerField()
    job_counts = JobCountSerializer(many=True)


class JobSkillCountSerializer(serializers.Serializer):
    skill = serializers.CharField()
    jobs_count = serializers.IntegerField()


class HourlyJobSkillCountSerializer(serializers.Serializer):
    hour = serializers.IntegerField()
    job_counts = JobSkillCountSerializer(many=True)


class DailyJobCountSerializer(serializers.Serializer):
    date = serializers.CharField()
    job_counts = serializers.ListField(
        child=serializers.IntegerField()
    )
