from flask import Flask, render_template
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
