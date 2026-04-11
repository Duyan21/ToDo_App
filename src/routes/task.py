import datetime

from src.utils.decorators.check_execute_time import check_execution_time
from src.utils.decorators.logging import log_api_decorator

now = datetime.datetime.now(datetime.timezone.utc)


from flask import Blueprint, redirect, render_template, request, jsonify, session
from src.database.models import db, Task, User

task_bp = Blueprint('task', __name__, template_folder='../../templates')


@task_bp.route("/tasks")
def task_page():
    user_id = session.get('user_id')
    if not user_id:
        return redirect("/register-signin")

    user = User.query.get(user_id)
    tasks = Task.query.filter_by(user_id=user_id).all()
    return render_template("tasks.html", tasks=tasks, user=user)


@task_bp.route('/api/task', methods=['POST'])
@check_execution_time
@log_api_decorator
def create_task():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Bạn cần đăng nhập để tạo task"}), 401

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
def update_task_status(task_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Bạn cần đăng nhập"}), 401

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
def get_tasks():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Bạn cần đăng nhập"}), 401

    filter_type = request.args.get('filter', 'all')
    query = Task.query.filter_by(user_id=user_id)

    if filter_type == 'completed':
        query = query.filter_by(status='Completed')
    elif filter_type == 'pending':
        query = query.filter_by(status='Pending')
    elif filter_type == 'overdue':
        now = datetime.datetime.now(datetime.timezone.utc)
        query = query.filter(Task.deadline < now, Task.status == 'Pending')

    tasks = query.all()
    tasks_data = []
    for task in tasks:
        tasks_data.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'deadline': task.deadline.isoformat() if task.deadline else None,
            'priority': task.priority,
            'status': task.status,
            'reminder_minutes': task.reminder_minutes
        })

    return jsonify({'tasks': tasks_data})


@task_bp.route('/api/task/<int:task_id>', methods=['PATCH'])
def edit_task(task_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Bạn cần đăng nhập"}), 401

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task không tồn tại"}), 404

    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'deadline' in data:
        task.deadline = datetime.datetime.strptime(data['deadline'], "%Y-%m-%d") if data['deadline'] else None
    if 'priority' in data:
        task.priority = data['priority']
    if 'reminder_minutes' in data:
        task.reminder_minutes = int(data['reminder_minutes'])

    db.session.commit()
    return jsonify({"message": "Task updated successfully"})


@task_bp.route('/api/task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({"error": "Bạn cần đăng nhập"}), 401

    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    if not task:
        return jsonify({"error": "Task không tồn tại"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted successfully"})


