# 🧾 CRM Automation – Celery + Redis + GraphQL

This Django project integrates **Celery** with **Redis** to automate background tasks like generating CRM reports via GraphQL queries.

---

## 📦 Requirements

- Python 3.10+
- Redis (as the Celery broker)
- PostgreSQL or SQLite (depending on your Django setup)
- Pipenv or virtualenv (recommended)

---

## ⚙️ Installation

### 1. Clone the project

```bash
git clone <repo-url>
cd crm
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Redis locally

#### 📦 On Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install redis
sudo systemctl start redis
```

#### 🍎 On macOS (with Homebrew)

```bash
brew install redis
brew services start redis
```

#### 🪟 On Windows

- Download from: https://github.com/microsoftarchive/redis/releases
- Install and run `redis-server.exe`

---

## 🔄 Run Django Migrations

```bash
python manage.py migrate
```

---

## 🚀 Start Celery Workers

### 1. Start the Celery worker

```bash
celery -A crm worker -l info
```

### 2. Start Celery Beat (if used)

```bash
celery -A crm beat -l info
```

Celery Beat schedules periodic tasks.

---

## 📈 Check the Logs

CRM reports are automatically generated and logged to:

```
/tmp/crm_report_log.txt
```

### 📄 Example entry:

```
[2025-07-24 12:00:00] ✅ Report: 153 customers, 289 orders, 41253.75 €
```

---

## 🛠 Manually Trigger the Task (optional)

Inside Django shell:

```bash
python manage.py shell
```

```python
from crm.tasks import generate_crm_report
generate_crm_report.delay()
```

---

## 🧹 Reset Cronjobs (if using `django-crontab`)

```bash
python manage.py crontab remove
python manage.py crontab add
```

---

## 📬 Questions?

Feel free to open an **Issue** or **Pull Request** if you'd like to contribute!
