from django.contrib import admin

from .models import Skill


class SkillAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    readonly_fields = ('slug',)


admin.site.register(Skill, SkillAdmin)
