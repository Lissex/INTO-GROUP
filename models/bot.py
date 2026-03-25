from .database import get_db

class Bot:
    @staticmethod
    def get_all_by_user(user_id):
        db = get_db()
        return db.execute('SELECT * FROM bots WHERE user_id = ?', (user_id,)).fetchall()

    @staticmethod
    def create(user_id, bot_name, bot_token):
        db = get_db()
        db.execute(
            'INSERT INTO bots (user_id, bot_name, bot_token) VALUES (?, ?, ?)',
            (user_id, bot_name, bot_token)
        )
        db.commit()
        return db.execute('SELECT * FROM bots WHERE rowid = last_insert_rowid()').fetchone()

    @staticmethod
    def delete(bot_id, user_id):
        db = get_db()
        db.execute('DELETE FROM bots WHERE id = ? AND user_id = ?', (bot_id, user_id))
        db.commit()

    @staticmethod
    def update_status(bot_id, user_id, is_active):
        db = get_db()
        db.execute('UPDATE bots SET is_active = ? WHERE id = ? AND user_id = ?', 
                  (int(is_active), bot_id, user_id))
        db.commit()