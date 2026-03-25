from flask import session, request
from flask_socketio import emit, join_room, leave_room
import time

from models.database import get_db


chat_messages = {}

def register_socket_handlers(socketio):
    @socketio.on('connect')
    def socket_connect():
        if 'user_id' not in session:
            return False
        db = get_db()
        clients = db.execute("SELECT * FROM clients").fetchall()
        emit('chats_list', [
            {"chat_id": c["id"], "chat_name": c["name"]} for c in clients
        ])

    @socketio.on('join_chat')
    def on_join(data):
        chat_id = data.get('chat_id')
        join_room(chat_id)
        messages = chat_messages.get(chat_id, [])
        emit('chat_history', messages, room=request.sid)

    @socketio.on('send_message')
    def on_send_message(data):
        chat_id = data.get('chat_id')
        text = data.get('message')
        user_name = session.get('user_name')
        msg = {
            "message_id": len(chat_messages.get(chat_id, [])) + 1,
            "chat_id": chat_id,
            "text": text,
            "is_from_bot": False,
            "user_name": user_name,
            "timestamp": time.time() * 1000
        }
        chat_messages.setdefault(chat_id, []).append(msg)
        emit('new_message', msg, room=chat_id)

    @socketio.on('load_more_messages')
    def on_load_more(data):
        chat_id = data.get('chat_id')
        before_ts = data.get('before_ts')
        messages = chat_messages.get(chat_id, [])
        older_msgs = [m for m in messages if m['timestamp'] < before_ts]
        older_msgs = older_msgs[-30:]
        emit('more_messages', older_msgs, room=request.sid)