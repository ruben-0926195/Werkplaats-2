import json
import os
from models.database import Database

db_path = 'databases/database.db'

def process_json(file):
    if not os.path.exists(db_path):
        return {"error": f"Database file {db_path} does not exist."}

    if not file or file.filename == '':
        return {"error": "No file selected."}

    if not file.filename.endswith('.json'):
        return {"error": "Uploaded file is not a JSON file."}

    try:
        json_data = json.load(file)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON format: {e}"}

    db = Database(db_path)
    cursor, connection = db.connect_db()

    try:
        # Check if the data is being read properly
        if not json_data:
            return {"error": "Uploaded JSON is empty or invalid."}

        # Insert each question into the database
        for question in json_data:
            try:
                sql = '''INSERT INTO questions (questions_id, prompts_id, users_id, question, answer, vak, onderwijsniveau, leerjaar, question_index, taxonomy_bloom, rtti) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                val = (
                    question['question_id'],
                    0,
                    '',
                    question['question'],
                    question.get('answer', ''),
                    question['vak'],
                    question['onderwijsniveau'],
                    question['leerjaar'],
                    question.get('question_index'),
                    None,
                    None
                )
                cursor.execute(sql, val)
            except Exception as e:
                return {"error": f"Error inserting question: {e}"}

        connection.commit()
    except Exception as e:
        return {"error": f"Database insertion error: {e}"}
    finally:
        db.close_connection()

    return {"success": "JSON data successfully uploaded and inserted into the database."}
