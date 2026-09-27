import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import attendance.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(help_text='Unique college ID for the student, e.g. STU2024001', max_length=20, unique=True)),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15, validators=[attendance.models.phone_validator])),
                ('course', models.CharField(help_text='e.g. B.Sc Computer Science', max_length=100)),
                ('semester', models.PositiveSmallIntegerField(choices=[(1, 'Semester 1'), (2, 'Semester 2'), (3, 'Semester 3'), (4, 'Semester 4'), (5, 'Semester 5'), (6, 'Semester 6'), (7, 'Semester 7'), (8, 'Semester 8')])),
                ('division', models.CharField(help_text='e.g. A, B, C', max_length=10)),
                ('roll_number', models.PositiveIntegerField(help_text='Roll number of the student within their class', validators=[django.core.validators.MinValueValidator(1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['course', 'semester', 'division', 'roll_number'],
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(choices=[('Present', 'Present'), ('Absent', 'Absent')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attendance_records', to='attendance.student')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddConstraint(
            model_name='student',
            constraint=models.UniqueConstraint(fields=('course', 'semester', 'division', 'roll_number'), name='unique_roll_number_per_class'),
        ),
        migrations.AddConstraint(
            model_name='attendance',
            constraint=models.UniqueConstraint(fields=('student', 'date'), name='unique_attendance_per_student_per_day'),
        ),
    ]
