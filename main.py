from flask import Flask, render_template
from models.user import User

app = Flask(__name__)

@app.route('/')
def overview():
    data = User()
    users = data.get_all_users()
    # This will render the overview.html template and pass 'users' to it
    return render_template('overview.html', users=users)



if __name__ == "__main__":
    app.run(debug=True)
