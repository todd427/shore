# Shore — Django Web Project

**Shore** is a Django-based web application structured for modular app development. It includes a custom user model, global and per-app templates, and follows Django best practices.

## 📦 Features

- Django 5.2+ with Python 3.12
- Custom user authentication (`accounts` app)
- Home page and static routes (`pages` app)
- Centralized templates directory (`templates/base.html`)
- Bootstrap-compatible template-ready layout
- Supports login/logout and extensible user workflows

---

## 🚀 Quickstart

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd shore
```

### 2. Create a virtual environment

```bash
python3 -m venv sandy
source sandy/bin/activate
```

> 📝 This project assumes your venv is named `sandy`, but you can name it anything.

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

(If `requirements.txt` is missing, install Django manually with `pip install django`.)

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to set up admin login.

### 6. Run the development server

```bash
python manage.py runserver
```

Visit: http://localhost:8000/

---

## 🗂️ Project Structure

```text
shore/
├── manage.py
├── shore/                 # Project settings module
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/              # Custom user model and auth views
├── pages/                 # Static pages and homepage
├── templates/             # Global templates
│   └── base.html
├── static/                # CSS/JS/images
```

---

## 🛠 Development Notes

- Templates are stored globally in `templates/` and extended with `{% extends "base.html" %}`.
- To create a new app:

  ```bash
  python manage.py startapp your_app_name
  ```

- Don't forget to register it in `INSTALLED_APPS`.

---

## ✅ To Do

- Add unit tests
- Set up deployment configuration (e.g. Railway, Render, Docker)
- Expand account features (registration, profile editing, etc.)

---

## 📄 License

MIT License (or add your preferred license here)

