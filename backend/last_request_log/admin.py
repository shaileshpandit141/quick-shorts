from django.contrib import admin
from .models import LastRequestLog

class LastRequestLogAdmin(admin.ModelAdmin):
    """Django admin interface for user request logs.

    Configures display, filtering and search for request tracking.
    """
    list_display = ('user', 'path', 'method', 'ip', 'timestamp', 'response_time', 
                   'is_authenticated', 'is_api_request', 'is_request_success')
    list_filter = ('method', 'is_authenticated', 'is_api_request', 'is_request_success') 
    search_fields = ('user', 'path', 'ip')

admin.site.register(LastRequestLog, LastRequestLogAdmin)
