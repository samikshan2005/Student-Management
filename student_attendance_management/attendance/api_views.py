from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Attendance, Student
from .serializers import (
    AttendanceSerializer,
    StudentAttendancePercentageSerializer,
    StudentSerializer,
)


class StudentViewSet(viewsets.ModelViewSet):
    """
    Full CRUD API for students, plus two extra actions:

    * /api/students/<id>/history/    -> this student's attendance history
    * /api/students/<id>/percentage/ -> this student's attendance percentage
    """
    queryset = Student.objects.all().order_by('name')
    serializer_class = StudentSerializer
    filterset_fields = ['course', 'semester', 'division']
    search_fields = ['name', 'student_id', 'email']

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        student = self.get_object()
        records = student.attendance_records.all().order_by('-date')
        serializer = AttendanceSerializer(records, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def percentage(self, request, pk=None):
        student = self.get_object()
        serializer = StudentAttendancePercentageSerializer(student)
        return Response(serializer.data)


class AttendanceViewSet(viewsets.ModelViewSet):
    """
    Full CRUD API for attendance records.

    Supports filtering via query params, e.g.:
    * /api/attendance/?date=2024-01-15
    * /api/attendance/?student=3
    """
    queryset = Attendance.objects.select_related('student').all().order_by('-date')
    serializer_class = AttendanceSerializer
    filterset_fields = ['date', 'status', 'student']

    @action(detail=False, methods=['get'], url_path='by-date/(?P<date>[\\d-]+)')
    def by_date(self, request, date=None):
        records = self.get_queryset().filter(date=date)
        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)


class AttendancePercentageListView(viewsets.ReadOnlyModelViewSet):
    """
    Read-only endpoint returning attendance-percentage figures for every
    student in one call: /api/attendance-percentage/
    """
    queryset = Student.objects.all().order_by('name')
    serializer_class = StudentAttendancePercentageSerializer
