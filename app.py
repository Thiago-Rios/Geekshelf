import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flqprwqe:3n0mkft13qCefWX3ZLDx8313X6LdBzX5@kesavan.db.elephantsql.com/flqprwqe'
db = SQLAlchemy(app)

@app.route('/', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html')

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    return render_template('cadastro.html')

@app.route('/adicao', methods=['GET','POST'])
def adicao():

    return render_template('adicao.html')

@app.route('/remocao', methods=["GET", "POST"])
def remocao():
    return render_template('remocao.html')

@app.route('/produto', methods=["GET", "POST"])
def produto():
    return render_template('produto.html')

if __name__ == '__main__':
    app.run(debug=True)