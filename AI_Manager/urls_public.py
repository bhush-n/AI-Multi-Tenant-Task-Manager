"""
URL configuration for the public schema only (e.g. localhost:8000).
Tenant app URLs (task_manager) are not included here.
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path


def public_home(request):
    """Landing for public schema - e.g. 'Choose your tenant' or marketing."""
    return HttpResponse(
        "<h1>Welcome</h1><p>This is the public site. Use a tenant subdomain to access the task manager.</p>",
        content_type="text/html",
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", public_home),
]
