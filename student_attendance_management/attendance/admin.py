from django.contrib import admin

from .models import Attendance, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id', 'name', 'email', 'course',
        'semester', 'division', 'roll_number', 'attendance_percentage_display',
    )
    list_filter = ('course', 'semester', 'division')
    search_fields = ('student_id', 'name', 'email')
    ordering = ('course', 'semester', 'division', 'roll_number')

    @admin.display(description='Attendance %')
    def attendance_percentage_display(self, obj):
        percentage = obj.attendance_percentage
        return f"{percentage}%" if percentage is not None else "No data"


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('student__name', 'student__student_id')
    ordering = ('-date',)
    autocomplete_fields = ('student',)


# autocomplete_fields on AttendanceAdmin requires search_fields on StudentAdmin,
# which is already configured above.
