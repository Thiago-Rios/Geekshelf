import os
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html')

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    return render_template('cadastro.html')

@app.route('/adicao', methods=["GET", "POST"])
def adicao():
    return render_template('adicao.html')

@app.route('/remocao', methods=["GET", "POST"])
def remocao():
    return render_template('remocao.html')

if __name__ == '__main__':
    app.run(debug=True)