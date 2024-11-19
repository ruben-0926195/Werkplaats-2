from flask import Flask, render_template, request, redirect, url_for, flash
from models.user import User

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key


@app.route('/', methods=['GET', 'POST'])
def overview():

    data = User()

    # Check if a POST request was made else load users without filters
    if request.method == "POST":
        # Access POST data as a MultiDict
        filters = request.form

        # Pass filters to the data layer
        users = data.get_all_users(filters)

        return render_template('overview.html', users=users)

    # Pass filters to the data layer
    users = data.get_all_users()

    return render_template('overview.html', users=users)

@app.route('/user/<user_id>')
def user_show(user_id):
    data = User()
    user = data.get_single_user(user_id)
    return render_template('user_show.html', user=user)


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


@app.route('/user/update/<user_id>', methods=['GET', 'POST'])
def user_update(user_id):
    user_model = User()

    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        display_name = request.form.get('display_name')
        is_admin = request.form.get('is_admin') == 'on'

        # Update the user based on whether a password is provided or not
        if password:
            user_model.update_user(user_id, login, password, display_name, is_admin)

        # Optionally, add a success message
        flash("User updated successfully!", "success")

        # Close the connection after updating the user
        user_model.close_connection()

        return redirect(url_for('overview'))

    # For GET request: Show the form pre-filled with user data
    user = user_model.get_single_user(user_id)

    # Close the connection after fetching user data
    user_model.close_connection()

    return render_template('user_update.html', user=user)


@app.route('/user/delete/<user_id>')
def user_delete(user_id):
    user_model = User()
    user_model.delete_user(user_id)

    return redirect(url_for('overview'))


if __name__ == "__main__":
    app.run(debug=True)
