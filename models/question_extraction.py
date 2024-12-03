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
        # Load and parse JSON
        json_data = json.load(file)
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON format: {e}"}

    # Debugging step to verify JSON parsing
    print(f"Loaded JSON Data: {json_data}")

    if not json_data:
        return {"error": "Uploaded JSON is empty or invalid."}

    # Connect to the database
    db = Database(db_path)
    cursor, connection = db.connect_db()

    try:
        # Insert each question into the database
        for question in json_data:
            try:
                # Ensure all required keys are present and set defaults for optional keys
                question_id = question.get('question_id', None)
                question_text = question.get('question', None)
                answer = question.get('answer', '')
                vak = question.get('vak', '')
                onderwijsniveau = question.get('onderwijsniveau', '')
                leerjaar = question.get('leerjaar', None)
                question_index = question.get('question_index', None)
                taxonomy_bloom = question.get('taxonomy_bloom', None)
                rtti = question.get('rtti', None)

                # Validate required fields
                if not question_id or not question_text:
                    raise ValueError("Missing required fields 'question_id' or 'question'.")

                sql = '''
                    INSERT INTO questions 
                    (questions_id, prompts_id, users_id, question, answer, vak, onderwijsniveau, leerjaar, question_index, taxonomy_bloom, rtti) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                val = (
                    question_id,  # questions_id
                    0,            # prompts_id
                    '',           # users_id
                    question_text,
                    answer,
                    vak,
                    onderwijsniveau,
                    leerjaar,
                    question_index,
                    taxonomy_bloom,
                    rtti
                )
                cursor.execute(sql, val)
            except Exception as e:
                # Log and skip problematic entries
                print(f"Error inserting question: {e}")
                continue

        connection.commit()
    except Exception as e:
        print(f"Database insertion error: {e}")
        return {"error": f"Database insertion error: {e}"}
    finally:
        db.close_connection()

    return {"success": "JSON data successfully uploaded and inserted into the database."}
