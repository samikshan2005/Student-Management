import datetime

from django.core.management.base import BaseCommand

from attendance.models import Attendance, Student


class Command(BaseCommand):
    help = "Loads sample/demo students and attendance records for testing the application."

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete all existing students and attendance records before loading sample data.',
        )

    def handle(self, *args, **options):
        if options['reset']:
            Attendance.objects.all().delete()
            Student.objects.all().delete()
            self.stdout.write(self.style.WARNING('Existing students and attendance records deleted.'))

        sample_students = [
            {
                'student_id': 'STU2024001', 'name': 'Aarav Sharma',
                'email': 'aarav.sharma@example.com', 'phone': '+919876543210',
                'course': 'B.Sc Computer Science', 'semester': 3, 'division': 'A', 'roll_number': 1,
            },
            {
                'student_id': 'STU2024002', 'name': 'Priya Patel',
                'email': 'priya.patel@example.com', 'phone': '+919876543211',
                'course': 'B.Sc Computer Science', 'semester': 3, 'division': 'A', 'roll_number': 2,
            },
            {
                'student_id': 'STU2024003', 'name': 'Rohan Mehta',
                'email': 'rohan.mehta@example.com', 'phone': '+919876543212',
                'course': 'B.Sc Computer Science', 'semester': 3, 'division': 'A', 'roll_number': 3,
            },
            {
                'student_id': 'STU2024004', 'name': 'Sneha Iyer',
                'email': 'sneha.iyer@example.com', 'phone': '+919876543213',
                'course': 'BCA', 'semester': 2, 'division': 'B', 'roll_number': 1,
            },
            {
                'student_id': 'STU2024005', 'name': 'Karan Verma',
                'email': 'karan.verma@example.com', 'phone': '+919876543214',
                'course': 'BCA', 'semester': 2, 'division': 'B', 'roll_number': 2,
            },
        ]

        created_students = []
        for data in sample_students:
            student, created = Student.objects.get_or_create(
                student_id=data['student_id'], defaults=data
            )
            created_students.append(student)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created student: {student.name}"))
            else:
                self.stdout.write(f"Student already exists: {student.name}")

        # Create attendance records for the last 10 days for each student,
        # with a simple alternating pattern so both Present and Absent
        # records exist.
        today = datetime.date.today()
        records_created = 0
        for index, student in enumerate(created_students):
            for day_offset in range(10):
                record_date = today - datetime.timedelta(days=day_offset)
                status = Attendance.ABSENT if (day_offset + index) % 4 == 0 else Attendance.PRESENT
                _, created = Attendance.objects.get_or_create(
                    student=student,
                    date=record_date,
                    defaults={'status': status},
                )
                if created:
                    records_created += 1

        self.stdout.write(self.style.SUCCESS(
            f"Sample data loaded: {len(created_students)} students, {records_created} attendance records created."
        ))
