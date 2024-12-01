from flask import Blueprint, render_template, request, jsonify

from models.question_extraction import process_json
from models.vragen_Models import Questions
from models.prompt import Prompt

question_routes = Blueprint('question', __name__)


@question_routes.route('/question/question_indexing')
def question_indexing():
    return "question_indexing"


@question_routes.route('/question/overview')
def question_overview():
    data = Questions()
    questions = data.get_all_questions()

    return render_template("question_overview.html", questions=questions)


@question_routes.route('/question/<question_id>')
def question_show(question_id):
    data = Questions()
    question = data.get_single_question(question_id)

    prompt = Prompt()
    prompts = prompt.get_prompts()

    return render_template('question_show.html', question=question, prompts=prompts)


@question_routes.route('/question/upload')
def upload_page():
    return render_template('upload.html')


@question_routes.route('/question/upload', methods=['POST'])
def upload_json():
    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({"error": "No file selected."}), 400


    result = process_json(file)


    if "error" in result:
        return render_template('upload.html', result=result)
    return render_template('upload.html', result=result)