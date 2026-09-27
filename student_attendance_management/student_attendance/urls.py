"""
URL configuration for the student_attendance project.

The `attendance` app owns both the HTML pages and the REST API,
so this file simply includes it twice: once at the site root for
the web pages, and once under /api/ for the REST endpoints.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('attendance.api_urls')),
    path('', include('attendance.urls')),
]
