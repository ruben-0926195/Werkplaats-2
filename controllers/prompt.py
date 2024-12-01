from flask import Blueprint, render_template, request, redirect, url_for, session
from models.prompt import Prompt


prompt_routes = Blueprint('prompt', __name__)

@prompt_routes.route('/prompt/overview', methods=['GET', 'POST'])
def prompt_overview():
    data = Prompt()

    page = int(request.args.get('page', 1))  # Default page is 1
    per_page = int(request.args.get('per_page', 5))  # Default 10 items per page

    # Check if a POST request was made else load users without filters
    if request.method == "POST":
        # Access POST data as a MultiDict
        filters = request.form

        # Store in session
        session['filters'] = filters

        # Pass filters to the data layer
        prompts, total_prompts = data.get_all_prompts(page, per_page, filters)

        total_pages = (total_prompts + per_page - 1) // per_page

        return render_template('prompt_overview.html',
                               prompts=prompts, page=page, per_page=per_page, total_pages=total_pages)

    # Retrieve filters from session to ensure consistent pagination results
    filters = session.get('filters', {})

    # Pass filters to the data layer
    prompts, total_prompts = data.get_all_prompts(page, per_page, filters)

    total_pages = (total_prompts + per_page - 1) // per_page

    return render_template('prompt_overview.html',
                           prompts=prompts, page=page, per_page=per_page, total_pages=total_pages)

@prompt_routes.route('/prompt/<prompt_id>')
def prompt_show(prompt_id):
    data = Prompt()
    prompt = data.get_single_prompt(prompt_id)
    return render_template('prompt_show.html', prompt=prompt)

@prompt_routes.route('/prompt/create', methods=['GET', 'POST'])
def prompt_create():
    if request.method == 'POST':
        title = request.form.get('prompt')
        prompt = request.form.get('prompt')

        prompt_model = Prompt()
        new_prompt = prompt_model.create_prompt(title, prompt)

        # Redirect after successful form submission
        if new_prompt:
            return redirect(url_for('prompt.prompt_overview'))
        else:
            message = "An error occurred. Please try again."
            return redirect(url_for('prompt.prompt_create'))

    return render_template('prompt_create.html')

@prompt_routes.route('/prompt/delete/<prompt_id>', methods=['GET', 'POST'])
def prompt_delete(prompt_id):
    data = Prompt()

    prompt = data.get_single_prompt(prompt_id)

    if request.method == 'POST':
        data.delete_prompt(prompt_id)
        message = "User deleted successfully!", "success"
        return redirect(url_for('prompt.prompt_overview'))

    # Pass the user object to the confirmation page
    return render_template('prompt_delete_modal.html', prompt=prompt)