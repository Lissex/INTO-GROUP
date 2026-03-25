from flask import Blueprint, request, session, jsonify, render_template
from decorator import login_required
from models.bot import Bot
from models.database import get_db

bots_bp = Blueprint('bots', __name__)

@bots_bp.route('/bots')
@login_required
def bots_page():
    return render_template('bots.html')

@bots_bp.route('/api/v1/bots', methods=['GET', 'POST'])
@login_required
def bots_api():
    user_id = session['user_id']

    if request.method == 'GET':
        bots = Bot.get_all_by_user(user_id)
        bots_list = []
        for b in bots:
            bots_list.append({
                "id": b['id'],
                "bot_name": b['bot_name'],
                "bot_token": b['bot_token'],
                "is_active": bool(b['is_active']),
                "created_at": b['created_at']
            })
        return jsonify(bots_list)

    elif request.method == 'POST':
        data = request.json
        bot_name = data.get('bot_name', 'Без имени')
        bot_token = data.get('bot_token')

        if not bot_token:
            return jsonify({"error": "Token бота обязателен"}), 400

        new_bot = Bot.create(user_id, bot_name, bot_token)
        return jsonify({
            "id": new_bot['id'],
            "bot_name": new_bot['bot_name'],
            "bot_token": new_bot['bot_token'],
            "is_active": bool(new_bot['is_active']),
            "created_at": new_bot['created_at']
        }), 201

@bots_bp.route('/api/v1/bots/<int:bot_id>', methods=['DELETE', 'PATCH'])
@login_required
def bot_detail(bot_id):
    user_id = session['user_id']

    if request.method == 'DELETE':
        Bot.delete(bot_id, user_id)
        return jsonify({"success": True})

    elif request.method == 'PATCH':
        data = request.json
        is_active = data.get('is_active')
        if is_active is None:
            return jsonify({"error": "Не указан новый статус"}), 400
        Bot.update_status(bot_id, user_id, is_active)
        return jsonify({"success": True})

@bots_bp.route('/api/v1/user/bots/active')
@login_required
def api_user_bots():
    return jsonify([
        {"id": 1, "bot_name": "Бот поддержки"},
        {"id": 2, "bot_name": "Бот продаж"}
    ])


@bots_bp.route('/api/v1/user/bots/active')
@login_required
def api_user_active_bots():
    db = get_db()
    user_id = session["user_id"]
    bots = db.execute(
        "SELECT * FROM bots WHERE user_id = ? AND is_active = 1", (user_id,)
    ).fetchall()
    return jsonify([
        {"id": b["id"], "bot_name": b["bot_name"]}
        for b in bots
    ])