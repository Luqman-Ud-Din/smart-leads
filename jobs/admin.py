from django.contrib import admin
from django.db.models import Count, Q

from services.db.queries import construct_search_query, construct_date_query
from skills.models import Skill
from .models import Job, JobSkill, JobSearchTerm


class SkillListFilter(admin.SimpleListFilter):
    title = 'skill'
    parameter_name = 'skill'

    def lookups(self, request, model_admin):
        start_date = request.GET.get('published_date__gte')
        end_date = request.GET.get('published_date__lte')
        selected_skill_id = self.value()
        search_query = request.GET.get('q')

        filters = []

        if start_date or end_date:
            filters.append(construct_date_query(start_date, end_date, 'job__published_date'))

        if search_query:
            search_fields = ['job__url', 'job__description']
            filters.append(construct_search_query(search_query, search_fields))

        combined_query = Q.create(filters, connector=Q.AND)

        job_skills = JobSkill.objects.filter(combined_query)

        # Get the top 100 skills based on job count within the filtered job skills
        top_skills = Skill.objects.filter(
            job_skills__in=job_skills
        ).annotate(
            job_count=Count('job_skills')
        ).order_by('-job_count')[:100]

        lookups = [(skill.id, f"{skill.name} ({skill.job_count})") for skill in top_skills]

        # Include the selected skill if it is not in the top 100
        if selected_skill_id:
            try:
                selected_skill = Skill.objects.get(id=selected_skill_id)
                if selected_skill.id not in [skill.id for skill in top_skills]:
                    job_count = job_skills.filter(skill=selected_skill).count()
                    lookups.append((selected_skill.id, f"{selected_skill.name} ({job_count})"))
            except Skill.DoesNotExist:
                pass

        return lookups

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(job_skills__skill_id=self.value())
        return queryset


class JobAdmin(admin.ModelAdmin):
    list_display = ('published_date', 'url', 'get_skills')
    list_filter = ('published_date', SkillListFilter)
    search_fields = ('url', 'description')

    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])

    get_skills.short_description = 'Skills'


admin.site.register(Job, JobAdmin)
admin.site.register(JobSkill)
admin.site.register(JobSearchTerm)
