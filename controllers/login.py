from flask import Blueprint, render_template, request, redirect, url_for, session

from lib.helpers import verify_password
from models.user import User
from extensions import limiter

login_routes = Blueprint('login', __name__)


@login_routes.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute", methods=["POST"])
def login():
    if "logged_in" in session:
        return redirect(url_for('question.question_overview'))
    else:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User()
            user_data = user.get_user_by_name(username)

            if user_data and verify_password(user_data['password'], password):
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = user_data['user_id']
                session['is_admin'] = user_data['is_admin']
                return redirect(url_for('question.question_overview'))
            else:
                print("wtf?")
                return render_template('login.html')

        return render_template('login.html')


@login_routes.route('/logout')
def logout():
    session.pop('logged_in', False)
    session.pop('username', None)
    session.pop('is_admin', None)
    session.clear()
    return redirect(url_for('login.login'))
