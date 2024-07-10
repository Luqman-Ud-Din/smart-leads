from django.contrib import admin

from search_terms.models import SearchTerm


class SearchTermAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    readonly_fields = ('slug',)


admin.site.register(SearchTerm, SearchTermAdmin)
