from models.database import Database

class Prompt:
    def __init__(self):
        database = Database('./databases/database.db')
        self.cursor, self.con = database.connect_db()

    def get_all_prompts(self):
        return

    def create_prompt(self, prompt):
        print(prompt)
        self.cursor.execute(
            "INSERT into prompts (prompt) VALUES (?)",
            (prompt,))
        self.con.commit()
        return True