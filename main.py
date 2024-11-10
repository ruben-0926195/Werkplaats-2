from flask import Flask, render_template, request, redirect, url_for, flash
from models.user import User

app = Flask(__name__)

@app.route('/')
def overview():
    data = User()
    users = data.get_all_users()

    # This will render the overview.html template and pass 'users' to it
    return render_template('overview.html', users=users)


@app.route('/user/create', methods=['GET', 'POST'])
def user_create():
    if request.method == 'POST':
        # Retrieve form data
        login = request.form.get('login')
        password = request.form.get('password')
        display_name = request.form.get('display_name')
        is_admin = request.form.get('is_admin') == 'on'  # Checkbox is checked

        # Process the form data (save to database, etc.)
        user_model = User()
        new_user = user_model.create_user(login, password, display_name, is_admin)


        # Redirect after successful form submission
        if new_user:
            print("User registered successfully!")
            return redirect(url_for('overview'))
        else:
            print("An error occurred. Please try again.")
            return redirect(url_for('user_create'))

    return render_template('user_create.html')


@app.route('/delete_user/<user_id>')
def delete_task(user_id):
    user_model = User()
    user_model.delete_user(user_id)

    return redirect(url_for('overview'))



if __name__ == "__main__":
    app.run(debug=True)
