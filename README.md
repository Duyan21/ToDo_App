# Todo App

A simple Flask-based todo application with user authentication, task management, and reminder support.

<img width="1516" height="1429" alt="screencapture-127-0-0-1-5000-tasks-2026-04-05-20_16_08" src="https://github.com/user-attachments/assets/76a4878d-5e47-4468-9641-ef24dddbb47c" />

## Project structure

- `src/` - main Flask application
  - `app/` - application package
    - `__init__.py` - app factory and blueprint registration
    - `app.py` - Flask app entry point
  - `database/` - SQLAlchemy models
    - `models.py` - database models
    - `schema.sql` - SQL Server database schema
  - `routes/` - Flask route handlers
    - `auth.py` - registration, login, logout
    - `task.py` - task CRUD and filters
  - `templates/` - HTML templates
  - `static/` - CSS and JavaScript assets
    - `css/` - stylesheets
    - `js/` - JavaScript files
  - `tests/` - test files
- `venv/` - local Python virtual environment (ignored)
- `instance/` - instance folder for configurations (ignored)
- `requirements.txt` - Python dependencies
- `pytest.ini` - pytest configuration file

## Features

- User registration and login
- Create, edit, delete tasks
- Set task deadline and priority
- Add reminders for tasks
- Task status toggling and task filtering

## Requirements

- Python 3.10+ (or compatible)
- Flask
- Flask SQLAlchemy

## Setup

1. Clone the repository:

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd project_1
```

2. Create and activate a virtual environment:

Windows:
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

3. Installation Instructions

To install the required Python packages for this project, run the following command:

```bash
pip install -r requirements.txt
```

If you want to install additional packages, you can use the following command (replace `flask` with the desired package name):

```bash
npm install flask
```

4. Setup database (SQL Server):
 - Open SQL Server Management Studio (SSMS)
 - Open file:
    - database/schema.sql
    - Click Execute to create database and tables

5. Create .env file in the root folder:
 - DB_HOST=localhost\SQLEXPRESS
 - DB_NAME=todo_app_db
 - DB_DRIVER={ODBC Driver 17 for SQL Server}

This project uses Windows Authentication, so no username/password is required.
Make sure your Windows account has access to SQL Server.

6. Run the application:

```bash
python main.py
```

7. Open the app in your browser:

```
http://127.0.0.1:5000/register-signin
```

## Notes

- The local SQLite database file is ignored by `.gitignore`.
- If you add more dependencies, create a `requirements.txt` file with `pip freeze > requirements.txt`.

## License

This repository is ready to upload to GitHub. Add a license file if needed.
