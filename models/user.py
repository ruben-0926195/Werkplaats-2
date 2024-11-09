from models.database import Database

class User:
    def __init__(self):
        database = Database('./databases/database.db')
        self.cursor, self.con = database.connect_db()

    def get_all_users(self):
        result = self.cursor.execute("SELECT * FROM users").fetchall()
        return result