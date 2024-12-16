import json

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash, send_file

from models.prompt import Prompt
from models.question import Questions
from models.question_extraction import process_json

question_routes = Blueprint('question', __name__)


def create_export_file():
    data = Questions()
    all_questions = data.get_handeld_questions()
    file_path = "export_files/questions_export.json"

    with open(file_path, "w") as f:
        for question in all_questions:
            f.write(json.dumps(dict(question)) + ",")
            data.delete_question(question["questions_id"])
        f.close()


@question_routes.route('/question/download')
def export_questions():
    create_export_file()
    file_path = "export_files/questions_export.json"
    return send_file(file_path, as_attachment=True)


@question_routes.route('/question/question_indexing')
def question_indexing():
    if "logged_in" not in session:
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
    if "logged_in" not in session:
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
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    data = Questions()
    question = data.get_single_question(question_id)

    prompt = Prompt()
    prompts = prompt.get_prompts()

    return render_template('question_show.html', question=question, prompts=prompts)


@question_routes.route('/question/delete/<question_id>', methods=['GET', 'POST'])
def question_delete(question_id):
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    if session["is_admin"] == 0:
        return redirect(url_for('question.question_overview'))

    data = Questions()

    question = data.get_single_question(question_id)

    if request.method == 'POST':
        data.delete_question(question_id)
        flash("Question deleted successfully!", "delete")
        return redirect(url_for('question.question_overview'))

    return render_template('question_delete_modal.html', question=question)


@question_routes.route('/question/upload')
def upload_page():
    if "logged_in" not in session:
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

@question_routes.route('/question/update/<questions_id>', methods=['GET', 'POST'])
def question_update(questions_id):
    # Ensure the user is logged in
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    question_model = Questions()

    if request.method == 'POST':
        # Collect data from the form
        prompts_id = request.form.get('prompts_id')
        users_id = request.form.get('users_id')  # Capture the new users_id from dropdown
        question = request.form.get('question')
        taxonomy_bloom = request.form.get('taxonomy_bloom')
        rtti = request.form.get('rtti')
        tax_bloom_changed = request.form.get('tax_bloom_changed') == 'on'
        rtti_changed = request.form.get('rtti_changed') == 'on'

        # Update the question in the database
        question_model.update_question(
            questions_id, prompts_id, users_id, question,
            taxonomy_bloom, rtti, tax_bloom_changed, rtti_changed
        )

        flash("Question updated successfully!", "update")

        # Close the database connection
        question_model.close_connection()

        return redirect(url_for('question.question_overview'))

    question = question_model.get_single_question(questions_id)
    users = question_model.get_all_users()  # Fetch all users for dropdown

    # Close the database connection after fetching the data
    question_model.close_connection()

    return render_template('question_update.html', question=question, users=users)