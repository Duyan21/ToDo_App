from src.app import create_app
from src.database import db
from dotenv import load_dotenv
load_dotenv()

from apscheduler.schedulers.background import BackgroundScheduler
from src.jobs.scheduler import process_notifications, check_overdue_tasks

app = create_app()

def process_all():
    process_notifications()
    check_overdue_tasks()

with app.app_context():
    db.create_all()

    scheduler = BackgroundScheduler()
    scheduler.add_job(process_all, 'interval', seconds=5)
    scheduler.start()

if __name__ == "__main__":
    app.run(debug=True)