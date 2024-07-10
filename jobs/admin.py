from django.contrib import admin

from skills.models import Skill
from .models import Job, JobSkill, JobSearchTerm


class SkillListFilter(admin.SimpleListFilter):
    title = 'skill'
    parameter_name = 'skill'

    def lookups(self, request, model_admin):
        skills = Skill.objects.all()
        return [(skill.id, skill.name) for skill in skills]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(skills__id=self.value())
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
