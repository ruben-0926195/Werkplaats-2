from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def overview():
    message = "Hello, this is your Flask app's homepage!"
    # This will render the index.html template and pass 'message' to it
    return render_template('base.html', message=message)

if __name__ == "__main__":
    app.run(debug=True)
