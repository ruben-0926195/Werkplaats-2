from flask import Flask, render_template, request, redirect, url_for, flash
from models.user import User
import hashlib

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Replace with a strong secret key

# Static salt for simplicity (replace with dynamic salting for better security)
STATIC_SALT = "static_salt_12345"


def hash_password(password):
    """Hash the password with a static salt."""
    return hashlib.sha256((STATIC_SALT + password).encode()).hexdigest()


@app.route('/', methods=['GET', 'POST'])
def overview():
    data = User()

    page = int(request.args.get('page', 1))  # Default page is 1
    per_page = int(request.args.get('per_page', 5))  # Default 10 items per page

    # Check if a POST request was made else load users without filters
    if request.method == "POST":
        # Access POST data as a MultiDict
        filters = request.form

        # Pass filters to the data layer
        users, total_users = data.get_all_users(page, per_page, filters)

        total_pages = (total_users + per_page - 1) // per_page

        return render_template('overview.html',
                               users=users, page=page, per_page=per_page, total_pages=total_pages)

    # Pass filters to the data layer
    users, total_users = data.get_all_users(page, per_page)

    total_pages = (total_users + per_page - 1) // per_page

    return render_template('overview.html',
                           users=users, page=page, per_page=per_page, total_pages=total_pages)


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

        # Hash the password before saving
        hashed_password = hash_password(password)

        # Process the form data (save to database, etc.)
        user_model = User()
        new_user = user_model.create_user(login, hashed_password, display_name, is_admin)

        # Redirect after successful form submission
        if new_user:
            flash("User registered successfully!", "success")
            return redirect(url_for('overview'))
        else:
            flash("An error occurred. Please try again.", "danger")
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

        # Hash the password if provided
        hashed_password = hash_password(password) if password else None
        user_model.update_user(user_id, login, hashed_password, display_name, is_admin)

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


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')

        # Fetch user by login
        user_model = User()
        user = user_model.get_user_by_login(login)

        if not user:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

        # Verify the hashed password
        hashed_password = hash_password(password)
        if user['password'] == hashed_password:
            flash("Login successful!", "success")
            return redirect(url_for('overview'))
        else:
            flash("Invalid username or password.", "danger")
            return redirect(url_for('login'))

    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)
