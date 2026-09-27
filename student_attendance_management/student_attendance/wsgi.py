"""
WSGI config for the student_attendance project.

It exposes the WSGI callable as a module-level variable named ``application``.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_attendance.settings')

application = get_wsgi_application()
