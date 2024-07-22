from django.contrib import admin
from django.contrib.admin import DateFieldListFilter
from django.db.models import Q, Count, OuterRef, Subquery, F
from rangefilter.filters import NumericRangeFilter, DateRangeFilter

from services.db.queries import (
    construct_search_query, construct_date_query,
    construct_numeric_range_query, filter_empty_q_objects
)
from skills.models import Skill
from .models import Job, JobSkill, JobSearchTerm


class SkillListFilter(admin.SimpleListFilter):
    title = 'skill'
    parameter_name = 'skill'

    def lookups(self, request, model_admin):
        start_date = request.GET.get('published_date__gte') or request.GET.get('published_date__range__gte')
        end_date = request.GET.get('published_date__lt') or request.GET.get('published_date__range__lte')
        search_query = request.GET.get('q')
        budget_amount_min = request.GET.get('budget_amount__range__gte')
        budget_amount_max = request.GET.get('budget_amount__range__lte')
        budget_min_rate_min = request.GET.get('budget_min_rate__range__gte')
        budget_min_rate_max = request.GET.get('budget_min_rate__range__lte')
        budget_max_rate_min = request.GET.get('budget_max_rate__range__gte')
        budget_max_rate_max = request.GET.get('budget_max_rate__range__lte')
        budget_type = request.GET.get('budget_type__exact')

        selected_skill_id = self.value()
        if selected_skill_id:
            selected_skill_id = int(selected_skill_id)

        filters = []

        if start_date or end_date:
            filters.append(construct_date_query(start_date, end_date, 'published_date'))

        if search_query:
            search_fields = ['url', 'description']
            filters.append(construct_search_query(search_query, search_fields))

        if budget_amount_min or budget_amount_max:
            filters.append(
                construct_numeric_range_query(
                    budget_amount_min,
                    budget_amount_max,
                    'budget_amount'
                )
            )

        if budget_min_rate_min or budget_min_rate_max:
            filters.append(
                construct_numeric_range_query(
                    budget_min_rate_min,
                    budget_min_rate_max,
                    'budget_min_rate'
                )
            )

        if budget_max_rate_min or budget_max_rate_max:
            filters.append(
                construct_numeric_range_query(
                    budget_max_rate_min,
                    budget_max_rate_max,
                    'budget_max_rate'
                )
            )

        if budget_type:
            filters.append(Q(budget_type=budget_type))

        if selected_skill_id:
            filters.append(Q(job_skills__skill_id=selected_skill_id))

        filters = filter_empty_q_objects(filters)

        combined_query = Q.create(filters, connector=Q.AND)

        top_skills_limit = 50
        if combined_query.children:
            skill_subquery = Skill.objects.filter(id=OuterRef('job_skills__skill_id'))
            top_skills = (
                Job.objects.filter(combined_query)
                .annotate(skill_id=F('job_skills__skill_id'))
                .filter(job_skills__skill_id=Subquery(skill_subquery.values('id')))
                .values('job_skills__skill', 'job_skills__skill__name')
                .annotate(job_count=Count('job_skills__skill'))
                .order_by('-job_count')[:top_skills_limit]
            )
        else:
            top_skills = (
                Job.objects.annotate(skill_id=F('job_skills__skill_id'))
                .values('job_skills__skill', 'job_skills__skill__name')
                .annotate(job_count=Count('job_skills'))
                .order_by('-job_count')[:top_skills_limit]
            )

        lookups = [
            (skill['job_skills__skill'], f"{skill['job_skills__skill__name']} ({skill['job_count']})")
            for skill in top_skills
        ]

        # Include the selected skill if it is not in the top 50
        if selected_skill_id and not any(skill_id == selected_skill_id for skill_id, _ in lookups):
            selected_skill = Skill.objects.get(id=selected_skill_id)
            try:
                selected_skill_count = Job.objects.filter(
                    combined_query
                ).values(
                    'job_skills__skill', 'job_skills__skill__name'
                ).annotate(
                    job_count=Count('job_skills')
                ).get(id=selected_skill_id)

                lookups.append((selected_skill.id, f"{selected_skill.name} ({selected_skill_count.job_count})"))
            except Job.DoesNotExist:
                lookups.append((selected_skill.id, f"{selected_skill.name} (0)"))

        return lookups

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(job_skills__skill_id=self.value())
        return queryset


class JobAdmin(admin.ModelAdmin):
    list_display = (
        'published_date', 'url', 'get_skills',
        'budget_type', 'budget_amount', 'budget_min_rate', 'budget_max_rate'
    )
    list_filter = (
        ('published_date', DateFieldListFilter),  # Default date filters
        ('published_date', DateRangeFilter),  # Custom date range filter
        'budget_type',
        ('budget_amount', NumericRangeFilter),
        ('budget_min_rate', NumericRangeFilter),
        ('budget_max_rate', NumericRangeFilter),
        SkillListFilter,
    )
    search_fields = ('url', 'description')
    ordering = ('-published_date',)

    def get_skills(self, obj):
        return ", ".join([skill.name for skill in obj.skills.all()])

    get_skills.short_description = 'Skills'


admin.site.register(Job, JobAdmin)
admin.site.register(JobSkill)
admin.site.register(JobSearchTerm)
