from .database import get_db

class Task:
    @staticmethod
    def get_all_by_user(user_id):
        db = get_db()
        return db.execute('''
            SELECT tasks.*, clients.name AS client_name
            FROM tasks LEFT JOIN clients ON tasks.client_id = clients.id
            WHERE tasks.user_id = ?
        ''', (user_id,)).fetchall()

    @staticmethod
    def create(data, user_id):
        db = get_db()
        db.execute(
            "INSERT INTO tasks (name, client_id, user_id, description, status, deadline, planned_time) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                data.get("name"),
                data.get("client_id"),
                user_id,
                data.get("description"),
                data.get("status"),
                data.get("deadline"),
                data.get("planned_time")
            )
        )
        db.commit()