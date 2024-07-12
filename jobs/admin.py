from django.contrib import admin
from django.db.models import Count

from skills.models import Skill
from .models import Job, JobSkill, JobSearchTerm


class SkillListFilter(admin.SimpleListFilter):
    title = 'skill'
    parameter_name = 'skill'

    def lookups(self, request, model_admin):
        # Get the top 100 skills based on job count
        top_skills = Skill.objects.annotate(
            job_count=Count('job_skills')
        ).order_by('-job_count')[:100]
        # Return skill id, name and job count
        return [(skill.id, f"{skill.name} ({skill.job_count})") for skill in top_skills]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(job_skills__skill_id=self.value())
        return queryset


class JobAdmin(admin.ModelAdmin):
    list_display = ('published_date', 'url', 'get_skills')
    list_filter = ('published_date', SkillListFilter)
    search_fields = ('url',)

    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])

    get_skills.short_description = 'Skills'


admin.site.register(Job, JobAdmin)
admin.site.register(JobSkill)
admin.site.register(JobSearchTerm)
