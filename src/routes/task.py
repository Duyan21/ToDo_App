import datetime

from src.utils.decorators.check_execute_time import check_execution_time
from src.utils.decorators.logging import log_api_decorator
from src.utils.decorators.require_auth import require_auth
from flask import Blueprint, redirect, render_template, request, jsonify, session
from src.database.models import db, Task, User

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
    user_id = session.get('user_id')

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    deadline = data.get('deadline')
    priority = data.get('priority')
    reminder_minutes = data.get('reminder_minutes', 0)

    new_task = Task(
        user_id=user_id,
        title=title,
        description=description,
        deadline=datetime.datetime.strptime(
            deadline, "%Y-%m-%d") if deadline else None,
        priority=priority,
        reminder_minutes=int(reminder_minutes),
        status="Pending",
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task created successfully"})


@task_bp.route('/api/task/<int:task_id>', methods=['PUT'])
@require_auth
def update_task_status(task_id):
    user_id = session.get('user_id')

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task không tồn tại"}), 404

    data = request.get_json()
    new_status = data.get('status')

    if new_status == "Completed":
        task.status = "Completed"
        task.completed_at = datetime.datetime.now(datetime.timezone.utc)
    elif new_status == "Pending":
        task.status = "Pending"
        task.completed_at = None

    db.session.commit()
    return jsonify({"message": "Task updated successfully"})


@task_bp.route('/api/tasks', methods=['GET'])
@require_auth
def get_tasks():
    user_id = session.get('user_id')

    filter_type = request.args.get('filter', 'all')
    query = Task.query.filter_by(user_id=user_id)

    filters = {
        'completed': lambda q: q.filter_by(status='Completed'),
        'pending': lambda q: q.filter_by(status='Pending'),
        'overdue': lambda q: q.filter(Task.deadline < datetime.datetime.now(datetime.timezone.utc), Task.status == 'Pending')
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

    tasks_data = list(map(lambda t: {
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'deadline': t.deadline.isoformat() if t.deadline else None,
        'priority': t.priority,
        'status': t.status,
        'reminder_minutes': t.reminder_minutes
    }, tasks))

    return jsonify({'tasks': tasks_data})


@task_bp.route('/api/task/<int:task_id>', methods=['PATCH'])
@require_auth
def edit_task(task_id):
    user_id = session.get('user_id')

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task không tồn tại"}), 404

    data = request.get_json()

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'deadline' in data:
        task.deadline = datetime.datetime.strptime(
            data['deadline'], "%Y-%m-%d") if data['deadline'] else None
    if 'priority' in data:
        task.priority = data['priority']
    if 'reminder_minutes' in data:
        task.reminder_minutes = int(data['reminder_minutes'])

    db.session.commit()
    return jsonify({"message": "Task updated successfully"})


@task_bp.route('/api/task/<int:task_id>', methods=['DELETE'])
@require_auth
def delete_task(task_id):
    user_id = session.get('user_id')

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task không tồn tại"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})
