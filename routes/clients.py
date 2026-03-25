from flask import Blueprint, request, jsonify
from decorator import login_required
from models.database import get_db

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/api/v1/clients', methods=['GET'])
@login_required
def api_clients():
    db = get_db()
    clients = db.execute("SELECT * FROM clients").fetchall()
    return jsonify([
        {"id": c["id"], "name": c["name"]}
        for c in clients
    ])

@clients_bp.route('/api/v1/clients', methods=['POST'])
@login_required
def api_create_client():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Имя клиента обязательно"}), 400

    db = get_db()
    db.execute("INSERT INTO clients (name) VALUES (?)", (name,))
    db.commit()

    client = db.execute("SELECT * FROM clients ORDER BY id DESC LIMIT 1").fetchone()

    return jsonify({"id": client["id"], "name": client["name"]}), 201