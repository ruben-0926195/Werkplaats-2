from models.database import Database

class User:
    def __init__(self):
        database = Database('./databases/database.db')
        self.cursor, self.con = database.connect_db()

    def get_all_users(self):
        result = self.cursor.execute("SELECT * FROM users").fetchall()
        return result

    def get_single_user(self, user_id):
        result = self.cursor.execute("SELECT * FROM users WHERE user_id=?", (str(user_id),)).fetchone()
        return result

    def create_user(self, login, password, display_name, is_admin):
        self.cursor.execute(
            "INSERT into users (login,password,display_name,is_admin) VALUES (?,?,?,?)",
            (login, password, display_name, is_admin))
        self.con.commit()
        return True

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE user_id=?", (str(user_id),))
        self.con.commit()

