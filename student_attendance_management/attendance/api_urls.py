from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import api_views

router = DefaultRouter()
router.register(r'students', api_views.StudentViewSet, basename='student')
router.register(r'attendance', api_views.AttendanceViewSet, basename='attendance')
router.register(
    r'attendance-percentage',
    api_views.AttendancePercentageListView,
    basename='attendance-percentage',
)

urlpatterns = [
    path('', include(router.urls)),
]
