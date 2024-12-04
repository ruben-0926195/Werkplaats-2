from flask import Blueprint, render_template, request, redirect, url_for, session
from models.user import User

login_routes = Blueprint('login', __name__)

@login_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User()

        username_check = user.check_user_in_db(username)
        password_check = user.check_pasw_in_db(password)
        if username_check and password_check:
            return redirect(url_for('question.question_overview'))
        else:
            return render_template('login.html')

    return render_template('login.html')

