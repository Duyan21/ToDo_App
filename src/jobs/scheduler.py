from datetime import datetime
from flask import current_app
from src.database.models import Notification, Task, db


def process_notifications():
    now = datetime.now()

    notifications = Notification.query.join(Task).filter(
        Notification.notify_time <= now,
        Notification.sent == False,
        Task.status != "Completed"
    ).all()

    for n in notifications:
        print(f"[NOTI] User {n.user_id}: {n.message}")
        n.sent = True

    db.session.commit()


def check_overdue_tasks():
    now = datetime.now()

    tasks = Task.query.filter(
        Task.deadline < now,
        Task.status == "Pending",
        Task.overdue_notified == False
    ).all()

    for task in tasks:
        Notification.query.filter_by(
            task_id=task.id,
            type="REMINDER"
        ).delete()

        notification = Notification(
            user_id=task.user_id,
            task_id=task.id,
            type="OVERDUE",
            message=f"Task '{task.title}' đã quá hạn",
            notify_time=now,
            sent=True
        )

        db.session.add(notification)
        task.overdue_notified = True

    db.session.commit()