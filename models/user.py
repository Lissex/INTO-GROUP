from .database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    @staticmethod
    def create(name, email, password):
        db = get_db()
        hashed_password = generate_password_hash(password)
        try:
            db.execute(
                'INSERT INTO users (name, email, password) VALUES (?, ?, ?)',
                (name, email, hashed_password)
            )
            db.commit()
            return db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        except Exception as e:
            raise e

    @staticmethod
    def get_by_email(email):
        db = get_db()
        return db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user['password'], password)
