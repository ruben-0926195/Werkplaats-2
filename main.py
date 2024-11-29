from flask import Flask
from controllers.user import user_routes
from controllers.question import question_routes
from controllers.prompt import prompt_routes

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key

app.register_blueprint(user_routes)
app.register_blueprint(question_routes)
app.register_blueprint(prompt_routes)


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         login = request.form.get('login')
#         password = request.form.get('password')
#
#         # Fetch user by login
#         user_model = User()
#         user = user_model.get_user_by_login(login)
#
#         if not user:
#             flash("Invalid username or password.", "danger")
#             return redirect(url_for('user.login'))
#
#         # Verify the hashed password
#         hashed_password = hash_password(password)
#         if user['password'] == hashed_password:
#             flash("Login successful!", "success")
#             return redirect(url_for('user.overview'))
#         else:
#             flash("Invalid username or password.", "danger")
#             return redirect(url_for('user.login'))
#
#     return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
