from flask import Blueprint, render_template, request, redirect, url_for, session
from models.prompt import Prompt

login_routes = Blueprint('login', __name__)

@login_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

def check_login(username, password):
    user
