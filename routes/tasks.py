from flask import Blueprint, request, session, jsonify, render_template
from decorator import login_required
from models.database import get_db
from models.task import Task

tasks_bp = Blueprint('tasks', __name__)  # Изменили на 'tasks'

@tasks_bp.route('/')
@login_required
def index():
    db = get_db()
    clients = db.execute('SELECT * FROM clients').fetchall()
    tasks = db.execute('''
        SELECT tasks.*, clients.name AS client_name
        FROM tasks LEFT JOIN clients ON tasks.client_id = clients.id
    ''').fetchall()
    user = {"id": session['user_id'], "name": session['user_name']}
    return render_template('main.html', user=user, clients=clients, tasks=tasks)

@tasks_bp.route('/api/v1/tasks', methods=['GET', 'POST'])
@login_required
def tasks_api():
    user_id = session['user_id']

    if request.method == 'GET':
        tasks = Task.get_all_by_user(user_id)
        task_list = [
            {
                "id": t['id'],
                "name": t['name'],
                "client": t['client_name'],
                "description": t['description'],
                "status": t['status'],
                "deadline": t['deadline'],
                "planned_time": t['planned_time']
            } for t in tasks
        ]
        return jsonify(task_list)
    
    elif request.method == 'POST':
        data = request.json
        Task.create(data, user_id)
        return jsonify({"success": True}), 201

@tasks_bp.route('/api/v1/user')
@login_required
def api_user():
    return jsonify({"id": session['user_id'], "name": session['user_name']})


@tasks_bp.route('/tasks')
@login_required
def tasks_page():
    db = get_db()
    user_id = session['user_id']

    tasks = db.execute('''
        SELECT tasks.*, clients.name AS client_name
        FROM tasks
        LEFT JOIN clients ON tasks.client_id = clients.id
        WHERE tasks.user_id = ?
        ORDER BY tasks.id DESC
    ''', (user_id,)).fetchall()

    clients = db.execute('SELECT * FROM clients').fetchall()

    user = {"id": user_id, "name": session['user_name']}
    return render_template("tasks.html", user=user, tasks=tasks, clients=clients)

@tasks_bp.route('/api/v1/tasks/<int:task_id>', methods=['GET'])
@login_required
def task_detail(task_id):
    db = get_db()
    user_id = session['user_id']

    task = db.execute('''
        SELECT tasks.*, clients.name AS client_name
        FROM tasks
        LEFT JOIN clients ON tasks.client_id = clients.id
        WHERE tasks.id = ? AND tasks.user_id = ?
    ''', (task_id, user_id)).fetchone()

    if not task:
        return jsonify({"error": "Задача не найдена"}), 404

    return jsonify({
        "id": task["id"],
        "name": task["name"],
        "client": task["client_name"],
        "description": task["description"],
        "status": task["status"],
        "deadline": task["deadline"]
    })

@tasks_bp.route('/api/v1/time', methods=['POST'])
@login_required
def time_add():
    data = request.json
    db = get_db()

    task_id = data.get("task_id")
    date = data.get("date")
    hours = data.get("hours")
    comment = data.get("comment", "")

    if not all([task_id, date, hours]):
        return jsonify({"error": "Не все поля заполнены"}), 400

    db.execute('''
        INSERT INTO time_entries (task_id, date, hours, comment)
        VALUES (?, ?, ?, ?)
    ''', (task_id, date, hours, comment))

    db.commit()

    return jsonify({"success": True})