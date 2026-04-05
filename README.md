# Todo App

A simple Flask-based todo application with user authentication, task management, and reminder support.

## Project structure

- `todo_app/` - main Flask application
  - `run.py` - Flask app entry point
  - `app/` - application package
    - `__init__.py` - app factory and blueprint registration
    - `models.py` - SQLAlchemy models
    - `routes/` - Flask route handlers
      - `auth.py` - registration, login, logout
      - `task.py` - task CRUD and filters
  - `templates/` - HTML templates
  - `static/` - CSS and JavaScript assets
- `venv/` - local Python virtual environment (ignored)
- `mydb.sqlite` - local SQLite database file (ignored)

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

3. Install dependencies:

```bash
pip install flask sqlalchemy
```

4. Run the application:

```bash
cd todo_app
python run.py
```

5. Open the app in your browser:

```
http://127.0.0.1:5000/
```

## Notes

- The local SQLite database file is ignored by `.gitignore`.
- If you add more dependencies, create a `requirements.txt` file with `pip freeze > requirements.txt`.

## License

This repository is ready to upload to GitHub. Add a license file if needed.
