from rest_framework import serializers

from .models import Attendance, Student


class StudentSerializer(serializers.ModelSerializer):
    total_attendance_days = serializers.IntegerField(read_only=True)
    present_days = serializers.IntegerField(read_only=True)
    absent_days = serializers.IntegerField(read_only=True)
    attendance_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id',
            'student_id',
            'name',
            'email',
            'phone',
            'course',
            'semester',
            'division',
            'roll_number',
            'created_at',
            'total_attendance_days',
            'present_days',
            'absent_days',
            'attendance_percentage',
        ]
        read_only_fields = ['id', 'created_at']

    def get_attendance_percentage(self, obj):
        return obj.attendance_percentage

    def validate_roll_number(self, value):
        if value <= 0:
            raise serializers.ValidationError("Roll number must be a positive number.")
        return value


class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_code = serializers.CharField(source='student.student_id', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id',
            'student',
            'student_name',
            'student_code',
            'date',
            'status',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        """
        Prevent duplicate attendance records for the same student on the
        same date. This runs both on create and update.
        """
        student = data.get('student') or getattr(self.instance, 'student', None)
        date = data.get('date') or getattr(self.instance, 'date', None)

        queryset = Attendance.objects.filter(student=student, date=date)
        if self.instance is not None:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "Attendance for this student on this date has already been recorded."
            )
        return data


class StudentAttendancePercentageSerializer(serializers.ModelSerializer):
    """A lightweight serializer used by the attendance-percentage report endpoint."""
    total_attendance_days = serializers.IntegerField(read_only=True)
    present_days = serializers.IntegerField(read_only=True)
    absent_days = serializers.IntegerField(read_only=True)
    attendance_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id',
            'student_id',
            'name',
            'total_attendance_days',
            'present_days',
            'absent_days',
            'attendance_percentage',
        ]

    def get_attendance_percentage(self, obj):
        return obj.attendance_percentage
