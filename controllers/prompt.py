from flask import Blueprint, render_template, request, redirect, url_for
from models.prompt import Prompt


prompt_routes = Blueprint('prompt', __name__)

@prompt_routes.route('/prompt/create', methods=['GET', 'POST'])
def prompt_create():
    if request.method == 'POST':
        prompt_text = request.form.get('prompt')

        prompt_model = Prompt()
        new_prompt = prompt_model.create_prompt(prompt_text)

        # Redirect after successful form submission
        if new_prompt:
            return redirect(url_for('prompt.overview'))
        else:
            message = "An error occurred. Please try again."
            return redirect(url_for('prompt.prompt_create'))

    return render_template('prompt_create.html')