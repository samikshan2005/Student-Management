import datetime

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Attendance, Student


def make_student(**overrides):
    defaults = {
        'student_id': 'STU0001',
        'name': 'Test Student',
        'email': 'test.student@example.com',
        'phone': '+911234567890',
        'course': 'B.Sc Computer Science',
        'semester': 1,
        'division': 'A',
        'roll_number': 1,
    }
    defaults.update(overrides)
    return Student.objects.create(**defaults)


# ---------------------------------------------------------------------------
# MODEL TESTS
# ---------------------------------------------------------------------------

class StudentModelTests(TestCase):
    def test_student_creation(self):
        student = make_student()
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(str(student), f"{student.name} ({student.student_id})")

    def test_student_update(self):
        student = make_student()
        student.name = 'Updated Name'
        student.save()
        student.refresh_from_db()
        self.assertEqual(student.name, 'Updated Name')

    def test_student_deletion(self):
        student = make_student()
        student_pk = student.pk
        student.delete()
        self.assertFalse(Student.objects.filter(pk=student_pk).exists())

    def test_attendance_percentage_with_no_records(self):
        student = make_student()
        self.assertIsNone(student.attendance_percentage)

    def test_attendance_percentage_calculation(self):
        student = make_student()
        today = datetime.date.today()
        Attendance.objects.create(student=student, date=today, status=Attendance.PRESENT)
        Attendance.objects.create(
            student=student, date=today - datetime.timedelta(days=1), status=Attendance.PRESENT
        )
        Attendance.objects.create(
            student=student, date=today - datetime.timedelta(days=2), status=Attendance.ABSENT
        )
        Attendance.objects.create(
            student=student, date=today - datetime.timedelta(days=3), status=Attendance.ABSENT
        )
        # 2 present out of 4 total = 50%
        self.assertEqual(student.total_attendance_days, 4)
        self.assertEqual(student.present_days, 2)
        self.assertEqual(student.absent_days, 2)
        self.assertEqual(student.attendance_percentage, 50.0)


class AttendanceModelTests(TestCase):
    def test_attendance_creation(self):
        student = make_student()
        record = Attendance.objects.create(
            student=student, date=datetime.date.today(), status=Attendance.PRESENT
        )
        self.assertEqual(Attendance.objects.count(), 1)
        self.assertEqual(record.status, Attendance.PRESENT)

    def test_duplicate_attendance_prevention(self):
        student = make_student()
        today = datetime.date.today()
        Attendance.objects.create(student=student, date=today, status=Attendance.PRESENT)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Attendance.objects.create(student=student, date=today, status=Attendance.ABSENT)


# ---------------------------------------------------------------------------
# API TESTS
# ---------------------------------------------------------------------------

class StudentAPITests(APITestCase):
    def test_create_student_via_api(self):
        url = reverse('student-list')
        payload = {
            'student_id': 'STU9001',
            'name': 'API Student',
            'email': 'api.student@example.com',
            'phone': '+919999999999',
            'course': 'BCA',
            'semester': 1,
            'division': 'A',
            'roll_number': 1,
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 1)

    def test_list_students_via_api(self):
        make_student()
        url = reverse('student-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_retrieve_update_delete_student_via_api(self):
        student = make_student()
        detail_url = reverse('student-detail', args=[student.pk])

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.patch(detail_url, {'name': 'Changed Name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        student.refresh_from_db()
        self.assertEqual(student.name, 'Changed Name')

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Student.objects.filter(pk=student.pk).exists())


class AttendanceAPITests(APITestCase):
    def test_create_attendance_via_api(self):
        student = make_student()
        url = reverse('attendance-list')
        payload = {'student': student.pk, 'date': str(datetime.date.today()), 'status': 'Present'}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 1)

    def test_duplicate_attendance_rejected_via_api(self):
        student = make_student()
        today = str(datetime.date.today())
        url = reverse('attendance-list')
        first = self.client.post(url, {'student': student.pk, 'date': today, 'status': 'Present'}, format='json')
        self.assertEqual(first.status_code, status.HTTP_201_CREATED)

        second = self.client.post(url, {'student': student.pk, 'date': today, 'status': 'Absent'}, format='json')
        self.assertEqual(second.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Attendance.objects.count(), 1)

    def test_student_percentage_endpoint(self):
        student = make_student()
        Attendance.objects.create(student=student, date=datetime.date.today(), status=Attendance.PRESENT)
        url = reverse('student-percentage', args=[student.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['attendance_percentage'], 100.0)
