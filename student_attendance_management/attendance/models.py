from django.core.validators import RegexValidator, MinValueValidator
from django.db import models


phone_validator = RegexValidator(
    regex=r'^\+?\d{7,15}$',
    message="Phone number must contain 7 to 15 digits, optionally starting with '+'."
)


class Student(models.Model):
    """Represents a single student enrolled in the college."""

    SEMESTER_CHOICES = [(i, f'Semester {i}') for i in range(1, 9)]

    student_id = models.CharField(
        max_length=20,
        unique=True,
        help_text="Unique college ID for the student, e.g. STU2024001",
    )
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, validators=[phone_validator])
    course = models.CharField(max_length=100, help_text="e.g. B.Sc Computer Science")
    semester = models.PositiveSmallIntegerField(choices=SEMESTER_CHOICES)
    division = models.CharField(max_length=10, help_text="e.g. A, B, C")
    roll_number = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text="Roll number of the student within their class",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['course', 'semester', 'division', 'roll_number']
        # A roll number only needs to be unique within the same
        # course/semester/division, not across the whole college.
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'semester', 'division', 'roll_number'],
                name='unique_roll_number_per_class',
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.student_id})"

    @property
    def total_attendance_days(self):
        return self.attendance_records.count()

    @property
    def present_days(self):
        return self.attendance_records.filter(status=Attendance.PRESENT).count()

    @property
    def absent_days(self):
        return self.attendance_records.filter(status=Attendance.ABSENT).count()

    @property
    def attendance_percentage(self):
        """
        Returns the attendance percentage rounded to 2 decimal places.
        Returns None when the student has no attendance records at all,
        so templates/serializers can display something like "No data yet"
        instead of a misleading 0%.
        """
        total = self.total_attendance_days
        if total == 0:
            return None
        return round((self.present_days / total) * 100, 2)


class Attendance(models.Model):
    """A single day's attendance record for one student."""

    PRESENT = 'Present'
    ABSENT = 'Absent'
    STATUS_CHOICES = [
        (PRESENT, 'Present'),
        (ABSENT, 'Absent'),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_records',
    )
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'date'],
                name='unique_attendance_per_student_per_day',
            )
        ]

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
