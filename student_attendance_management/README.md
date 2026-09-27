# Student Attendance Management System

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
```

---

## 5. Installation Steps

### Step 1 — Clone / extract the project

Extract the ZIP on your computer and open the `student_attendance_management` folder in VS Code.

### Step 2 — Create a virtual environment

```bash
python -m venv venv
```

### Step 3 — Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS / Linux:**
```bash
source venv/bin/activate
```

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5 — Apply database migrations

A migration file is already included, but running `makemigrations` first is a safe habit — it will simply report "No changes detected" if nothing has changed.

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6 — Create an admin (superuser) account

```bash
python manage.py createsuperuser
```
Follow the prompts to set a username, email, and password.

### Step 7 — (Optional) Load sample/demo data

```bash
python manage.py load_sample_data
```
This creates 5 demo students and 10 days of attendance history for each (mixing Present and Absent). Run it with `--reset` to wipe existing data first:
```bash
python manage.py load_sample_data --reset
```

### Step 8 — Run the development server

```bash
python manage.py runserver
```

Now open your browser at **http://127.0.0.1:8000/**

- Web app: http://127.0.0.1:8000/
- REST API root: http://127.0.0.1:8000/api/
- Django Admin: http://127.0.0.1:8000/admin/

---

## 6. API Endpoints

Base URL: `/api/`

### Students

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/students/` | List all students |
| POST | `/api/students/` | Create a student |
| GET | `/api/students/<id>/` | Retrieve one student |
| PUT/PATCH | `/api/students/<id>/` | Update a student |
| DELETE | `/api/students/<id>/` | Delete a student |
| GET | `/api/students/<id>/history/` | That student's full attendance history |
| GET | `/api/students/<id>/percentage/` | That student's attendance percentage summary |

### Attendance

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/attendance/` | List attendance records (filter with `?date=YYYY-MM-DD`, `?student=<id>`, `?status=Present`) |
| POST | `/api/attendance/` | Create an attendance record |
| GET | `/api/attendance/<id>/` | Retrieve one record |
| PUT/PATCH | `/api/attendance/<id>/` | Update a record |
| DELETE | `/api/attendance/<id>/` | Delete a record |
| GET | `/api/attendance/by-date/<YYYY-MM-DD>/` | All attendance records for a specific date |

### Reports

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/attendance-percentage/` | Attendance percentage for every student |

All endpoints return JSON and standard HTTP status codes (`200`, `201`, `204`, `400`, `404`).

---

## 7. How to Use the System

1. **Add students** from the "Students" page (or `POST /api/students/`).
2. **Mark attendance** from the "Attendance" page for a chosen student and date. Trying to mark the same student twice on the same date will show a clear validation error.
3. Check the **Dashboard** for a quick overview of totals and overall attendance percentage.
4. Open the **Report** page to see every student's total/present/absent days and attendance percentage.
5. Use the **Django Admin** (`/admin/`) for quick bulk management, searching, and filtering.

---

## 8. Testing Instructions

Run the full test suite with:

```bash
python manage.py test
```

The tests cover:
- Student creation, update, and deletion
- Attendance creation and duplicate-attendance prevention
- Attendance percentage calculation
- REST API CRUD behavior for students and attendance
- The duplicate-attendance rule enforced through the API

---

## 9. GitHub Upload Instructions

```bash
git init
git add .
git commit -m "Initial commit: Student Attendance Management System"
git branch -M main
git remote add origin <your-empty-github-repo-url>
git push -u origin main
```

The included `.gitignore` already excludes `venv/`, `__pycache__/`, `db.sqlite3`, `.env`, and other files that should not be committed.

---

## 10. Deployment Ready (for later)

This project is structured so it can be deployed later without restructuring:

- `requirements.txt` — includes `gunicorn` (WSGI server) and `whitenoise` (static file serving).
- `Procfile` — ready for Heroku-style platforms (`web: gunicorn student_attendance.wsgi`).
- Settings read `SECRET_KEY`, `DEBUG`, and `ALLOWED_HOSTS` from environment variables via `python-decouple`, with safe local defaults so nothing needs to be configured just to run it locally. See `.env.example` for the variables to set in production.
- `STATIC_ROOT` and WhiteNoise are configured so `python manage.py collectstatic` works out of the box when you're ready to deploy.

**This project has not been deployed** — deployment is left for you to do when you're ready.

---

## 11. Future Enhancements

- User authentication and role-based access (Admin / Teacher / Student logins).
- Email or SMS notifications for low attendance.
- Export attendance reports to PDF/Excel.
- Bulk attendance marking for an entire class in one action (e.g. a class roster checklist).
- Charts/graphs for attendance trends over time.
- Switch to PostgreSQL for production use.

---

## License

This project was built for educational purposes as a college assignment.
