# 🎓 Edu Hub – Student Management System Transfer to New Repo
📌 **New Repository:** [Edu Hub on GitHub](https://github.com/apl-mhd/edu-hub)  
🌍 **Live Demo (AWS EC2):** [http://3.89.205.102:3000/](http://3.89.205.102:3000/) 

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)  
[![Django](https://img.shields.io/badge/Django-4.x-green)](https://www.djangoproject.com/)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue)](https://www.postgresql.org/)  
[![Docker](https://img.shields.io/badge/Docker-Compose-blue)](https://www.docker.com/)  
[![Vue.js](https://img.shields.io/badge/Vue-3.2-brightgreen)](https://vuejs.org/)  
[![AWS](https://img.shields.io/badge/AWS-EC2-orange?logo=amazonaws&logoColor=white)](https://aws.amazon.com/ec2/)  
[![CI/CD](https://img.shields.io/badge/GitHub-Actions-blue?logo=githubactions&logoColor=white)](https://github.com/features/actions)   

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
- **Backend:** Python, Django, Django REST Framework  
- **Frontend:** Vue 3, Vue Router, Axios  
- **Database:** PostgreSQL  
- **Containerization:** Docker, Docker Compose  
- **Optional:** Celery + Redis for background tasks  
- **Deployment:** AWS EC2 + Nginx + GitHub Actions (CI/CD)  

---

## 🚀 Getting Started  

### Backend (Django) – Local Development  
```bash
# Clone repo
git clone https://github.com/apl-mhd/edu-hub.git
cd edu-hub

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
python manage.py createsuperuser

# Start backend server
python manage.py runserver
