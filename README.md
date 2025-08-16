# Edu – Student Management System

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.x-green)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](https://www.docker.com/)
[![Vue.js](https://img.shields.io/badge/Vue-3.2-brightgreen)](https://vuejs.org/)

A full-featured **Student Management System** for enrollment, payments, billing, reports, SMS notifications, and filtering. Built for easy deployment with Docker, Docker Compose, PostgreSQL, and Vue.js frontend.

---

## ✨ Features
- **Student Enrollment**: Add/update students, assign courses and sections.
- **Payments & Billing**: Track payments, partial payments, discounts, generate invoices.
- **Reports**: Generate reports by date, course, or section.
- **SMS Notifications**: Send payment receipts, reminders, or announcements.
- **Filtering & Search**: Filter students, payments, invoices, and reports.
- **Role-Based Access**: Admin, Accountant, Instructor.
- **Dockerized Deployment**: Run locally or in production with a single command.
- **Vue.js Frontend**: Responsive SPA for managing students and payments.

---

## 📦 Tech Stack
- **Backend**: Django + Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: Vue 3 + Vue Router + Axios
- **Containerization**: Docker + Docker Compose
- **Optional**: Celery + Redis for background tasks

---

## 🚀 Getting Started

### Backend (Django) – Local Development
```bash
# Clone repo
git clone https://github.com/yourusername/edu.git
cd edu

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python bmanage.py createsuperuser

# Start backend server
python manage.py runserver
