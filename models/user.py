from models.database import Database


class User:
    def __init__(self):
        database = Database('./databases/database.db')
        self.cursor, self.con = database.connect_db()

    def get_all_users(self, page, per_page, filters=None):

        offset = (page - 1) * per_page
        total_users = self.cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]

        query = "SELECT * FROM users WHERE 1=1"
        params = []

        if filters:
            # Apply filters
            if filters.get("user_id"):
                query += " AND user_id LIKE ?"
                params.append(f"%{filters['user_id']}%")
            if filters.get("login"):
                query += " AND login LIKE ?"
                params.append(f"%{filters['login']}%")
            if filters.get("password"):
                query += " AND password LIKE ?"
                params.append(f"%{filters['password']}%")
            if filters.get("display_name"):
                query += " AND display_name LIKE ?"
                params.append(f"%{filters['display_name']}%")
            if filters.get("is_admin"):
                query += " AND is_admin LIKE ?"
                params.append(f"%{filters['is_admin']}%")

        query += " LIMIT ? OFFSET ?"
        params.append(per_page)
        params.append(offset)

        # Execute the query
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()

        return result, total_users

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
