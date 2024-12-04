from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

from models.question_extraction import process_json
from models.question import Questions
from models.prompt import Prompt

question_routes = Blueprint('question', __name__)


@question_routes.route('/question/question_indexing')
def question_indexing():
    if "is_login" not in session:
        return redirect(url_for('login.login'))

    return "question_indexing"


# @question_routes.route('/question/overview')
# def question_overview_old():
#     data = Questions()
#     questions = data.get_all_questions()
#
#     return render_template("question_overview.html", questions=questions)

@question_routes.route('/question/overview', methods=['GET', 'POST'])
def question_overview():
    if "is_login" not in session:
        return redirect(url_for('login.login'))

    data = Questions()

    page = int(request.args.get('page', 1))  # Default page is 1
    per_page = int(request.args.get('per_page', 5))  # Default 10 items per page

    # Check if a POST request was made else load users without filters
    if request.method == "POST":
        # Access POST data as a MultiDict
        filters = request.form

        # Store in session
        session['filters'] = filters

        # Pass filters to the data layer
        questions, total_questions = data.get_all_questions(page, per_page, filters)

        total_pages = (total_questions + per_page - 1) // per_page

        return render_template('question_overview.html',
                               questions=questions, page=page, per_page=per_page, total_pages=total_pages)

    # Retrieve filters from session to ensure consistent pagination results
    filters = session.get('filters', {})

    # Pass filters to the data layer
    questions, total_questions = data.get_all_questions(page, per_page, filters)

    total_pages = (total_questions + per_page - 1) // per_page

    return render_template('question_overview.html',
                           questions=questions, page=page, per_page=per_page, total_pages=total_pages)

@question_routes.route('/question/<question_id>')
def question_show(question_id):
    if "is_login" not in session:
        return redirect(url_for('login.login'))

    data = Questions()
    question = data.get_single_question(question_id)

    prompt = Prompt()
    prompts = prompt.get_prompts()

    return render_template('question_show.html', question=question, prompts=prompts)


@question_routes.route('/question/upload')
def upload_page():
    if "is_login" not in session:
        return redirect(url_for('login.login'))

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