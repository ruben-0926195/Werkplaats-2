from models.database import Database


class Questions:
    def __init__(self):
        database = Database('./databases/database.db')
        self.cursor, self.con = database.connect_db()

    # def get_all_questions(self):
    #     result = self.cursor.execute("SELECT * FROM questions").fetchall()
    #     return result

    def get_all_questions(self, page, per_page, filters=None):

        offset = (page - 1) * per_page

        query_get_questions = "SELECT * FROM questions WHERE 1=1"
        query_get_total_questions = "SELECT COUNT(*) FROM questions WHERE 1=1"
        params = []

        if filters:
            # Apply filters
            if filters.get("questions_id"):
                query_get_questions += " AND questions_id LIKE ?"
                query_get_total_questions += " AND questions_id LIKE ?"
                params.append(f"%{filters['questions_id']}%")
            if filters.get("question"):
                query_get_questions += " AND question LIKE ?"
                query_get_total_questions += " AND question LIKE ?"
                params.append(f"%{filters['question']}%")
            if filters.get("vak"):
                query_get_questions += " AND vak LIKE ?"
                query_get_total_questions += " AND vak LIKE ?"
                params.append(f"%{filters['vak']}%")

        query_get_questions += " LIMIT ? OFFSET ?"
        params_get_questions = params + [per_page, offset]

        # Execute the query
        self.cursor.execute(query_get_questions, params_get_questions)
        result = self.cursor.fetchall()

        self.cursor.execute(query_get_total_questions, params)
        total_questions = self.cursor.fetchone()[0]

        return result, total_questions

    def get_single_question(self, question_id):
        self.cursor.execute("SELECT * FROM questions WHERE questions_id = ?", (question_id,))
        question = self.cursor.fetchone()
        return question

    def create_question(self, questions_id, prompts_id, users_id, question,
                        taxonomy_bloom, rtti, tax_bloom_changed,rtti_changed):
        self.cursor.execute(
            "INSERT into questions (questions_id,prompts_id,users_id, question, taxonomy_bloom, rtti, tax_bloom_changed, rtti_changed)VALUES (?,?,?,?,?,?,?,?)",
            (questions_id, prompts_id, users_id, question, taxonomy_bloom, rtti, tax_bloom_changed,rtti_changed))
        self.con.commit()
        return True

    def update_questions(self, questions_id, prompts_id, users_id, question,
                        taxonomy_bloom, rtti, tax_bloom_changed,rtti_changed):
        try:
            question = self.get_single_question(questions_id)

            if not question:
                print(f"Question with ID {questions_id} not found.")
                return None

            self.cursor.execute("""
                UPDATE questions
                SET questions_id = ?, prompts_id = ?, users_id = ?, question = ?, taxonomy_bloom = ?, rtti = ?, tax_bloom_changed = ?, rtti_changed = ?
                WHERE questions_id = ?
            """, (questions_id,prompts_id,users_id,users_id, question, taxonomy_bloom, rtti, tax_bloom_changed, rtti_changed))

            self.con.commit()
            return True
        except Exception as e:
            print(f"Error updating questions: {e}")
            return None

    def delete_question(self, questions_id):
        self.cursor.execute("DELETE FROM questions WHERE questions_id=?", (str(questions_id),))
        self.con.commit()

    def close_connection(self):
        # Close the database connection
        self.con.close()
