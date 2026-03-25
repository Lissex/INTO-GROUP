from flask import Flask, redirect
from flask_socketio import SocketIO
from config import Config
from models.database import init_db
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.bots import bots_bp
from routes.chat import chat_bp
from socket_handlers.chat_handlers import register_socket_handlers
from routes.clients import clients_bp 


app = Flask(__name__)
app.config.from_object(Config)

socketio = SocketIO(app, cors_allowed_origins="*")

# Регистрация blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(bots_bp)
app.register_blueprint(chat_bp)
app.register_blueprint(clients_bp)

# Регистрация обработчиков сокетов
register_socket_handlers(socketio)

# Обработчик 404 ошибки
@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')


# Инициализация БД при запуске приложения
with app.app_context():
    init_db()

if __name__ == '__main__':
    socketio.run(app, debug=True)