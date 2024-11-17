from models.database import Database


class User:
    def __init__(self):
        database = Database('./databases/database.db')
        self.cursor, self.con = database.connect_db()

    def get_all_users(self):
        result = self.cursor.execute("SELECT * FROM users").fetchall()
        return result

    def get_single_user(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user = self.cursor.fetchone()
        return user

    def create_user(self, login, password, display_name, is_admin):
        self.cursor.execute(
            "INSERT into users (login,password,display_name,is_admin) VALUES (?,?,?,?)",
            (login, password, display_name, is_admin))
        self.con.commit()
        return True

    def update_user(self, user_id, login, password, display_name, is_admin):
        try:
            user = self.get_single_user(user_id)

            if not user:
                print(f"User with ID {user_id} not found.")
                return None

            self.cursor.execute("""
                UPDATE users
                SET login = ?, password = ?, display_name = ?, is_admin = ?
                WHERE user_id = ?
            """, (login, password, display_name, is_admin, user_id))

            self.con.commit()
            return True
        except Exception as e:
            print(f"Error updating user: {e}")
            return None

    def delete_user(self, user_id):
        self.cursor.execute("DELETE FROM users WHERE user_id=?", (str(user_id),))
        self.con.commit()

    def close_connection(self):
        # Close the database connection
        self.con.close()
