from flask import Blueprint, render_template
from models.vragen_Models import Questions

question_routes = Blueprint('question', __name__)

@question_routes.route('/questions/qustion_indaxeren')
def qustion_indaxeren():
    return "question_indaxeren"

@question_routes.route('/questions/')
def questions_overview():
    data = Questions()
    questions = data.get_all_questions()

    return render_template("questions_overview.html", questions=questions)

@question_routes.route('/questions/<question_id>')
def question_show(question_id):
    data = Questions()
    question = data.get_single_question(question_id)
    return render_template('question_show.html', question=question)