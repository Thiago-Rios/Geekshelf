from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import src.entidades.db_operations as OperationsDB
from src.entidades.produto import Produto

app = Flask(__name__)
operations_db = OperationsDB.OperationsDB()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flqprwqe:3n0mkft13qCefWX3ZLDx8313X6LdBzX5@kesavan.db.elephantsql.com/flqprwqe'
db = SQLAlchemy(app)

@app.route('/', methods=["GET", "POST"])
def index():
    produtos = operations_db.get_all_products(db)

    return render_template('index.html',produtos = produtos)

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html')

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    return render_template('cadastro.html')

@app.route('/adicao', methods=['GET'])
def adicao():
    return render_template('adicao.html')

@app.route('/adicionar', methods=["POST"])
def adioncionar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    genero = request.form['genero']
    sinopse = request.form['sinopse']
    imagem = request.files['imagem']

    novo_produto = Produto.adicionar_produto(titulo, autor, genero, sinopse, imagem)

    db.session.add(novo_produto)
    db.session.commit()
    return render_template('adicao.html')

@app.route('/remocao', methods=["GET", "POST"])
def remocao():
    return render_template('remocao.html')

@app.route('/produto', methods=["GET", "POST"])
def produto():
    return render_template('produto.html')

if __name__ == '__main__':
    app.run(debug=True)