Student Attendance Management System

A simple, clean **Student Attendance Management System** built with **Python, Django, Django REST Framework, Bootstrap and SQLite**. Built as a college project — the code is intentionally kept beginner-friendly and well commented.

---

## 1. Project Description

This project lets a college manage students and their daily attendance through:

- A set of **Django template web pages** (dashboard, student CRUD, attendance CRUD, and a report page), and
- A full **REST API** (built with Django REST Framework) for the same data, so the system can later be integrated with a mobile app or another frontend.

It automatically calculates each student's **attendance percentage** and prevents duplicate attendance entries for the same student on the same day.

---

## 2. Features

- **Student Management** — add, view, update, and delete students.
- **Attendance Management** — mark, edit, delete, and view attendance, filterable by date and by student.
- **Duplicate prevention** — a student cannot have two attendance records for the same date (enforced at the database level, the form level, and the API level).
- **Attendance percentage** — calculated automatically for every student: `(Present Days / Total Days) × 100`.
- **Dashboard** — total students, total attendance records, present/absent counts, and overall attendance percentage.
- **Attendance Report page** — a per-student breakdown of total/present/absent days and attendance percentage, with a visual progress bar.
- **REST API** — full CRUD for students and attendance, plus extra endpoints for a student's attendance history and percentage.
- **Django Admin** — manage students and attendance with search, filters, and sorted list views.
- **Validation** — unique student ID, valid email, positive roll numbers, valid phone numbers, and duplicate-attendance prevention, all with clear error messages.
- **Sample data command** — one command loads 5 demo students with realistic attendance history.
- **Automated tests** — model, form, and API tests covering the core requirements.

---

## 3. Technologies Used

| Layer | Technology |
|---|---|
| Language | Python 3.x |
| Backend Framework | Django 5 |
| API | Django REST Framework |
| Database | SQLite (local) |
| Frontend | Django Templates + Bootstrap 5 |
| Static file serving | WhiteNoise (production-ready) |
| Config | python-decouple (`.env` support) |

---

## 4. Project Structure

```
student_attendance_management/
│
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── Procfile
│
├── templates/
│   └── base.html                 # Shared layout, navbar, Bootstrap
│
├── student_attendance/           # Project settings package
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── attendance/                   # Main application
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    ├── management/commands/
    │   └── load_sample_data.py   # Loads demo students + attendance
    ├── templates/attendance/     # Page templates (dashboard, CRUD, report)
    ├── static/attendance/css/    # Custom CSS
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py                 # Student, Attendance
    ├── forms.py                  # Django ModelForms for the web pages
    ├── serializers.py            # DRF serializers
    ├── views.py                  # Page views (dashboard, CRUD, report)
    ├── api_views.py              # DRF viewsets
    ├── urls.py                   # Web page URLs
    ├── api_urls.py               # REST API URLs
    └── tests.py
