import datetime

from src.utils.decorators.check_execute_time import check_execution_time
from src.utils.decorators.logging import log_api_decorator
from src.utils.decorators.require_auth import require_auth
from flask import Blueprint, redirect, render_template, request, jsonify, session
from src.database.models import db, Task, User, Notification
from src.dto import TaskCreateDTO, TaskUpdateDTO, TaskResponseDTO, NotificationResponseDTO
from src.dto.base import ValidationError

task_bp = Blueprint('task', __name__, template_folder='../../templates')


@task_bp.route("/tasks")
def task_page():
    user_id = session.get('user_id')
    if not user_id:
        return redirect("/")

    user = User.query.get(user_id)
    tasks = Task.query.filter_by(user_id=user_id).all()
    priority_order = {
        "High": 0,
        "Medium": 1,
        "Low": 2
    }
    tasks = sorted(tasks, key=lambda t: (
        priority_order[t.priority], t.created_at))
    return render_template("tasks.html", tasks=tasks, user=user)


@task_bp.route('/api/task', methods=['POST'])
@check_execution_time
@log_api_decorator
@require_auth
def create_task():
    try:
        user_id = session.get('user_id')
        data = request.get_json()
        
        task_dto = TaskCreateDTO(data)
        task_dto.validate()

        new_task = Task(
            user_id=user_id,
            title=task_dto.title,
            description=task_dto.description,
            deadline=task_dto.deadline,
            priority=task_dto.priority,
            reminder_minutes=task_dto.reminder_minutes,
            status="Pending",
            created_at=datetime.datetime.now()
        )
        db.session.add(new_task)
        db.session.commit()

        if new_task.deadline and new_task.reminder_minutes > 0:
            notify_time = new_task.deadline - \
                datetime.timedelta(minutes=new_task.reminder_minutes)

            notification = Notification(
                user_id=new_task.user_id,
                task_id=new_task.id,
                type="REMINDER",
                message=f"Task '{new_task.title}' sắp đến hạn",
                notify_time=notify_time,
                sent=False
            )

            db.session.add(notification)
            db.session.commit()

        task_response = TaskResponseDTO.from_model(new_task)
        return jsonify({
            "message": "Task created successfully",
            "task": task_response.to_dict()
        })
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to create task"}), 500


@task_bp.route('/api/task/<int:task_id>', methods=['PUT'])
@require_auth
def update_task_status(task_id):
    try:
        user_id = session.get('user_id')

        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({"error": "Task không tồn tại"}), 404

        data = request.get_json()
        update_dto = TaskUpdateDTO(data)
        update_dto.validate()
        
        if update_dto.status == "Completed":
            task.status = "Completed"
            task.completed_at = datetime.datetime.now(datetime.timezone.utc)
        elif update_dto.status == "Pending":
            task.status = "Pending"
            task.completed_at = None

        db.session.commit()
        
        task_response = TaskResponseDTO.from_model(task)
        return jsonify({
            "message": "Task updated successfully",
            "task": task_response.to_dict()
        })
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to update task"}), 500


@task_bp.route('/api/tasks', methods=['GET'])
@require_auth
def get_tasks():
    try:
        user_id = session.get('user_id')

        filter_type = request.args.get('filter', 'all')
        query = Task.query.filter_by(user_id=user_id)

        filters = {
            'completed': lambda q: q.filter_by(status='Completed'),
            'pending': lambda q: q.filter_by(status='Pending'),
            'overdue': lambda q: q.filter(Task.deadline < datetime.datetime.now(), Task.status == 'Pending')
        }

        query = filters.get(filter_type, lambda q: q)(query)
        tasks = query.all()

        priority_order = {
            'High': 0,
            'Medium': 1,
            'Low': 2
        }
        tasks = sorted(tasks, key=lambda t: (
            priority_order.get(t.priority), t.created_at))

        tasks_response = TaskResponseDTO.from_models_list(tasks)
        return jsonify({'tasks': [task.to_dict() for task in tasks_response]})
    except Exception as e:
        return jsonify({"error": "Failed to fetch tasks"}), 500


@task_bp.route('/api/task/<int:task_id>', methods=['PATCH'])
@require_auth
def edit_task(task_id):
    try:
        user_id = session.get('user_id')

        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({"error": "Task không tồn tại"}), 404

        data = request.get_json()
        update_dto = TaskUpdateDTO(data)
        update_dto.validate()

        # Update fields if they are provided in the DTO
        if update_dto.title is not None:
            task.title = update_dto.title
        if update_dto.description is not None:
            task.description = update_dto.description
        if update_dto.deadline is not None:
            task.deadline = update_dto.deadline
        if update_dto.priority is not None:
            task.priority = update_dto.priority
        if update_dto.reminder_minutes is not None:
            task.reminder_minutes = update_dto.reminder_minutes

        Notification.query.filter_by(
            task_id=task.id,
            type="REMINDER",
            sent=False
        ).delete()

        if task.deadline and task.reminder_minutes > 0:
            notify_time = task.deadline - \
                datetime.timedelta(minutes=task.reminder_minutes)

            new_notification = Notification(
                user_id=task.user_id,
                task_id=task.id,
                type="REMINDER",
                message=f"Task '{task.title}' sắp đến hạn",
                notify_time=notify_time,
                sent=False
            )

            db.session.add(new_notification)

        db.session.commit()
        
        task_response = TaskResponseDTO.from_model(task)
        return jsonify({
            "message": "Task updated successfully",
            "task": task_response.to_dict()
        })
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Failed to update task"}), 500


@task_bp.route('/api/task/<int:task_id>', methods=['DELETE'])
@require_auth
def delete_task(task_id):
    user_id = session.get('user_id')

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task không tồn tại"}), 404

    Notification.query.filter_by(task_id=task.id).delete()

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"})


@task_bp.route('/api/notifications', methods=['GET'])
@require_auth
def get_notifications():
    try:
        user_id = session.get('user_id')
        now = datetime.datetime.now()

        notifications = Notification.query.join(Task).filter(
            Notification.user_id == user_id,
            Notification.notify_time <= now,
            Notification.sent == True,
            Task.status != "Completed",
            (
                (Notification.type == "OVERDUE") |
                ((Notification.type == "REMINDER") & (Task.deadline >= now))
            )
        ).order_by(Notification.created_at.desc()).all()

        notifications_response = NotificationResponseDTO.from_models_list(notifications, now)
        return jsonify({
            "notifications": [notification.to_dict() for notification in notifications_response]
        })
    except Exception as e:
        return jsonify({"error": "Failed to fetch notifications"}), 500


@task_bp.route('/api/notifications/<int:id>/read', methods=['PATCH'])
@require_auth
def mark_read(id):
    n = Notification.query.get(id)

    if not n:
        return jsonify({"error": "Not found"}), 404

    n.is_read = True
    db.session.commit()

    return jsonify({"message": "ok"})


@task_bp.route('/api/notifications/read-all', methods=['PATCH'])
@require_auth
def mark_all_read():
    user_id = session.get('user_id')

    Notification.query.filter_by(
        user_id=user_id,
        is_read=False
    ).update({"is_read": True})

    db.session.commit()

    return jsonify({"message": "ok"})
