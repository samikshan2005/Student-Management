from django import forms

from .models import Attendance, Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'student_id', 'name', 'email', 'phone',
            'course', 'semester', 'division', 'roll_number',
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. STU2024001'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +919876543210'}),
            'course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. B.Sc Computer Science'}),
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'division': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. A'}),
            'roll_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'date', 'status']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data.get('student')
        date = cleaned_data.get('date')

        if student and date:
            queryset = Attendance.objects.filter(student=student, date=date)
            if self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError(
                    f"Attendance for {student.name} on {date} has already been recorded."
                )
        return cleaned_data


class AttendanceFilterForm(forms.Form):
    """Used on the attendance list page to filter by date and/or student."""
    date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    student = forms.ModelChoiceField(
        required=False,
        queryset=Student.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
