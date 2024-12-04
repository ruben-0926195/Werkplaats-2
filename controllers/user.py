from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from lib.helpers import hash_password

user_routes = Blueprint('user', __name__)


@user_routes.route('/', methods=['GET', 'POST'])
def overview():
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    if session["is_admin"] == 0:
        return redirect(url_for('question.question_overview'))


    data = User()

    page = int(request.args.get('page', 1))  # Default page is 1
    per_page = int(request.args.get('per_page', 5))  # Default 10 items per page

    # Check if a POST request was made else load users without filters
    if request.method == "POST":
        # Access POST data as a MultiDict
        filters = request.form

        # Store in session
        session['filters'] = filters

        # Pass filters to the data layer
        users, total_users = data.get_all_users(page, per_page, filters)

        total_pages = (total_users + per_page - 1) // per_page

        return render_template('overview.html',
                               users=users, page=page, per_page=per_page, total_pages=total_pages)

    # Retrieve filters from session to ensure consistent pagination results
    filters = session.get('filters', {})

    # Pass filters to the data layer
    users, total_users = data.get_all_users(page, per_page, filters)

    total_pages = (total_users + per_page - 1) // per_page

    return render_template('overview.html',
                           users=users, page=page, per_page=per_page, total_pages=total_pages)


@user_routes.route('/user/overview', methods=['GET', 'POST'])
def user_overview():
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    if session["is_admin"] == 0:
        return redirect(url_for('question.question_overview'))

    data = User()

    page = int(request.args.get('page', 1))  # Default page is 1
    per_page = int(request.args.get('per_page', 5))  # Default 10 items per page

    # Check if a POST request was made else load users without filters
    if request.method == "POST":
        # Access POST data as a MultiDict
        filters = request.form

        # Store in session
        session['filters'] = filters

        # Pass filters to the data layer
        users, total_users = data.get_all_users(page, per_page, filters)

        total_pages = (total_users + per_page - 1) // per_page

        return render_template('user_overview.html',
                               users=users, page=page, per_page=per_page, total_pages=total_pages)

    # Retrieve filters from session to ensure consistent pagination results
    filters = session.get('filters', {})

    # Pass filters to the data layer
    users, total_users = data.get_all_users(page, per_page, filters)

    total_pages = (total_users + per_page - 1) // per_page

    return render_template('user_overview.html',
                           users=users, page=page, per_page=per_page, total_pages=total_pages)


@user_routes.route('/user/<user_id>')
def user_show(user_id):
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    if session["is_admin"] == 0:
        return redirect(url_for('question.question_overview'))

    data = User()
    user = data.get_single_user(user_id)
    return render_template('user_show.html', user=user)


@user_routes.route('/user/create', methods=['GET', 'POST'])
def user_create():
    if "logged_in" not in session:
        return redirect(url_for('login.login'))
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
            return redirect(url_for('user.overview'))
        else:
            flash("An error occurred. Please try again.", "danger")
            return redirect(url_for('user.user_create'))

    return render_template('user_create.html')


@user_routes.route('/user/update/<user_id>', methods=['GET', 'POST'])
def user_update(user_id):
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    if session["is_admin"] == 0:
        return redirect(url_for('question.question_overview'))

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
        flash("User updated successfully!", "update")

        # Close the connection after updating the user
        user_model.close_connection()

        return redirect(url_for('user.overview'))

    # For GET request: Show the form pre-filled with user data
    user = user_model.get_single_user(user_id)

    # Close the connection after fetching user data
    user_model.close_connection()

    return render_template('user_update.html', user=user)


@user_routes.route('/user/delete/<user_id>', methods=['GET', 'POST'])
def user_delete(user_id):
    if "logged_in" not in session:
        return redirect(url_for('login.login'))

    if session["is_admin"] == 0:
        return redirect(url_for('question.question_overview'))

    data = User()

    # Fetch user by ID
    user = data.get_single_user(user_id)  # This should return the user object with `user_username` and `user_id`

    if request.method == 'POST':
        # Handle deletion
        data.delete_user(user_id)
        flash("User deleted successfully!", "delete")
        return redirect(url_for('user.overview'))

    # Pass the user object to the confirmation page
    return render_template('user_delete_modal.html', user=user)
