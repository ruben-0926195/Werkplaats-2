from models.database import Database

class Prompt:
    def __init__(self):
        database = Database('./databases/database.db')
        self.cursor, self.con = database.connect_db()

    def get_all_prompts(self, page, per_page, filters=None):

        offset = (page - 1) * per_page

        query_get_prompts = "SELECT * FROM prompts WHERE 1=1"
        query_get_total_prompts = "SELECT COUNT(*) FROM prompts WHERE 1=1"
        params = []

        if filters:
            # Apply filters
            if filters.get("prompts_id"):
                query_get_prompts += " AND prompts_id LIKE ?"
                query_get_total_prompts += " AND prompts_id LIKE ?"
                params.append(f"%{filters['prompts_id']}%")
            if filters.get("prompt"):
                query_get_prompts += " AND prompt LIKE ?"
                query_get_total_prompts += " AND prompt LIKE ?"
                params.append(f"%{filters['prompt']}%")

        query_get_prompts += " LIMIT ? OFFSET ?"
        params_get_prompts = params + [per_page, offset]

        # Execute the query
        self.cursor.execute(query_get_prompts, params_get_prompts)
        result = self.cursor.fetchall()

        self.cursor.execute(query_get_total_prompts, params)
        total_prompts = self.cursor.fetchone()[0]

        return result, total_prompts

    def create_prompt(self, prompt):
        print(prompt)
        self.cursor.execute(
            "INSERT into prompts (prompt) VALUES (?)",
            (prompt,))
        self.con.commit()
        return True