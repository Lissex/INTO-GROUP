from flask import Blueprint, render_template, jsonify
from decorator import login_required

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat')
@login_required
def chat_page():
    return render_template('chat.html')

@chat_bp.route('/api/v1/media/<file_id>')
@login_required
def api_media(file_id):
    return jsonify({"url": "/static/sample_media_placeholder.png"})