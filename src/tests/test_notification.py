import datetime
from src.database.models import db, Task, Notification
from src.jobs.scheduler import process_notifications, check_overdue_tasks


def create_task(user_id, deadline, reminder_minutes=0, status="Pending"):
    task = Task(
        user_id=user_id,
        title="Test Task",
        deadline=deadline,
        reminder_minutes=reminder_minutes,
        status=status,
        created_at=datetime.datetime.now()
    )
    db.session.add(task)
    db.session.commit()
    return task


def create_notification(user_id, task_id, type, notify_time, sent):
    n = Notification(
        user_id=user_id,
        task_id=task_id,
        type=type,
        message=type,
        notify_time=notify_time,
        sent=sent
    )
    db.session.add(n)
    db.session.commit()
    return n


def test_reminder_before_deadline(app_context, authenticated_client, test_user):
    now = datetime.datetime.now()

    task = create_task(
        test_user,
        deadline=now + datetime.timedelta(minutes=10),
        reminder_minutes=5
    )

    create_notification(
        test_user,
        task.id,
        "REMINDER",
        notify_time=now - datetime.timedelta(minutes=1),
        sent=True
    )

    res = authenticated_client.get("/api/notifications")
    data = res.get_json()["notifications"]

    assert len(data) == 1
    assert data[0]["type"] == "REMINDER"


def test_overdue_notification(app_context, authenticated_client, test_user):
    now = datetime.datetime.now()

    task = create_task(
        test_user,
        deadline=now - datetime.timedelta(minutes=5),
        reminder_minutes=5
    )

    check_overdue_tasks()

    res = authenticated_client.get("/api/notifications")
    data = res.get_json()["notifications"]

    assert len(data) == 1
    assert data[0]["type"] == "OVERDUE"


def test_no_duplicate_when_overdue(app_context, authenticated_client, test_user):
    now = datetime.datetime.now()

    task = create_task(
        test_user,
        deadline=now - datetime.timedelta(minutes=5),
        reminder_minutes=5
    )

    create_notification(
        test_user,
        task.id,
        "REMINDER",
        notify_time=now - datetime.timedelta(minutes=10),
        sent=True
    )

    check_overdue_tasks()

    res = authenticated_client.get("/api/notifications")
    data = res.get_json()["notifications"]

    assert len(data) == 1
    assert data[0]["type"] == "OVERDUE"


def test_no_notification_when_completed(app_context, authenticated_client, test_user):
    now = datetime.datetime.now()

    task = create_task(
        test_user,
        deadline=now - datetime.timedelta(minutes=5),
        reminder_minutes=5,
        status="Completed"
    )

    check_overdue_tasks()

    res = authenticated_client.get("/api/notifications")
    data = res.get_json()["notifications"]

    assert len(data) == 0


def test_notification_reappear_when_undo(app_context, authenticated_client, test_user):
    now = datetime.datetime.now()

    task = create_task(
        test_user,
        deadline=now - datetime.timedelta(minutes=5),
        reminder_minutes=5,
        status="Completed"
    )

    task.status = "Pending"
    db.session.commit()

    check_overdue_tasks()

    res = authenticated_client.get("/api/notifications")
    data = res.get_json()["notifications"]

    assert len(data) == 1
    assert data[0]["type"] == "OVERDUE"


def test_reminder_not_triggered_yet(app_context, authenticated_client, test_user):
    now = datetime.datetime.now()

    task = create_task(
        test_user,
        deadline=now + datetime.timedelta(minutes=10),
        reminder_minutes=5
    )

    create_notification(
        test_user,
        task.id,
        "REMINDER",
        notify_time=now + datetime.timedelta(minutes=2),
        sent=False
    )

    process_notifications()

    res = authenticated_client.get("/api/notifications")
    data = res.get_json()["notifications"]

    assert len(data) == 0


def test_reminder_triggered(app_context, authenticated_client, test_user):
    now = datetime.datetime.now()

    task = create_task(
        test_user,
        deadline=now + datetime.timedelta(minutes=10),
        reminder_minutes=5
    )

    create_notification(
        test_user,
        task.id,
        "REMINDER",
        notify_time=now - datetime.timedelta(minutes=1),
        sent=False
    )

    process_notifications()

    res = authenticated_client.get("/api/notifications")
    data = res.get_json()["notifications"]

    assert len(data) == 1
    assert data[0]["type"] == "REMINDER"