from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AttendanceFilterForm, AttendanceForm, StudentForm
from .models import Attendance, Student


# ---------------------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------------------

def dashboard(request):
    total_students = Student.objects.count()
    total_records = Attendance.objects.count()
    present_count = Attendance.objects.filter(status=Attendance.PRESENT).count()
    absent_count = Attendance.objects.filter(status=Attendance.ABSENT).count()

    overall_percentage = None
    if total_records > 0:
        overall_percentage = round((present_count / total_records) * 100, 2)

    recent_attendance = Attendance.objects.select_related('student').order_by('-date', '-created_at')[:8]

    context = {
        'total_students': total_students,
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'overall_percentage': overall_percentage,
        'recent_attendance': recent_attendance,
    }
    return render(request, 'attendance/dashboard.html', context)


# ---------------------------------------------------------------------------
# STUDENT CRUD
# ---------------------------------------------------------------------------

def student_list(request):
    query = request.GET.get('q', '').strip()
    students = Student.objects.all()
    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(course__icontains=query) |
            Q(email__icontains=query)
        )
    context = {'students': students, 'query': query}
    return render(request, 'attendance/student_list.html', context)


def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    records = student.attendance_records.all().order_by('-date')
    context = {
        'student': student,
        'records': records,
    }
    return render(request, 'attendance/student_detail.html', context)


def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(request, f"Student '{student.name}' was added successfully.")
            return redirect('student_list')
        messages.error(request, "Please correct the errors below.")
    else:
        form = StudentForm()
    return render(request, 'attendance/student_form.html', {'form': form, 'title': 'Add Student'})


def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, f"Student '{student.name}' was updated successfully.")
            return redirect('student_list')
        messages.error(request, "Please correct the errors below.")
    else:
        form = StudentForm(instance=student)
    return render(request, 'attendance/student_form.html', {'form': form, 'title': 'Edit Student'})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        name = student.name
        student.delete()
        messages.success(request, f"Student '{name}' was deleted successfully.")
        return redirect('student_list')
    return render(request, 'attendance/student_confirm_delete.html', {'student': student})


# ---------------------------------------------------------------------------
# ATTENDANCE CRUD
# ---------------------------------------------------------------------------

def attendance_list(request):
    records = Attendance.objects.select_related('student').all()
    filter_form = AttendanceFilterForm(request.GET or None)

    if filter_form.is_valid():
        date = filter_form.cleaned_data.get('date')
        student = filter_form.cleaned_data.get('student')
        if date:
            records = records.filter(date=date)
        if student:
            records = records.filter(student=student)

    context = {'records': records, 'filter_form': filter_form}
    return render(request, 'attendance/attendance_list.html', context)


def attendance_add(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(
                request,
                f"Attendance for '{record.student.name}' on {record.date} marked as {record.status}."
            )
            return redirect('attendance_list')
        messages.error(request, "Please correct the errors below.")
    else:
        form = AttendanceForm()
    return render(request, 'attendance/attendance_form.html', {'form': form, 'title': 'Mark Attendance'})


def attendance_edit(request, pk):
    record = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Attendance record updated successfully.")
            return redirect('attendance_list')
        messages.error(request, "Please correct the errors below.")
    else:
        form = AttendanceForm(instance=record)
    return render(request, 'attendance/attendance_form.html', {'form': form, 'title': 'Edit Attendance'})


def attendance_delete(request, pk):
    record = get_object_or_404(Attendance, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Attendance record deleted successfully.")
        return redirect('attendance_list')
    return render(request, 'attendance/attendance_confirm_delete.html', {'record': record})


# ---------------------------------------------------------------------------
# REPORTS
# ---------------------------------------------------------------------------

def attendance_report(request):
    students = Student.objects.annotate(
        total_days=Count('attendance_records'),
        present_days_count=Count('attendance_records', filter=Q(attendance_records__status=Attendance.PRESENT)),
    )
    report_rows = []
    for student in students:
        total = student.total_days
        present = student.present_days_count
        absent = total - present
        percentage = round((present / total) * 100, 2) if total > 0 else None
        report_rows.append({
            'student': student,
            'total': total,
            'present': present,
            'absent': absent,
            'percentage': percentage,
        })
    return render(request, 'attendance/attendance_report.html', {'report_rows': report_rows})
