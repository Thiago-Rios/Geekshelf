from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
#import src.entidades.db_operations as OperationsDB
from src.entidades.produto import Produto
from src.entidades.usuario import Usuario
from src.entidades.db_operations import db, OperationsDB

app = Flask(__name__)
operations_db = OperationsDB()
app.config['SECRET_KEY'] = 'seu_segredo_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flqprwqe:3n0mkft13qCefWX3ZLDx8313X6LdBzX5@kesavan.db.elephantsql.com/flqprwqe'
db.init_app(app)

@app.context_processor
def inject_usuario():
    usuario = None
    if 'user_id' in session:
        usuario = Usuario.query.get(session['user_id'])
    return dict(usuario=usuario)

@app.route('/', methods=["GET", "POST"])
def index():
    produtos = Produto.query.all()

    if 'user_id' in session:
        usuario = Usuario.query.filter_by(id=session['user_id']).first()
        return render_template('index.html',produtos = produtos, usuario = usuario)
    
    return render_template('index.html',produtos = produtos)

@app.route('/logout')
def logout():
    Usuario.realizar_logout(session)
    return redirect(url_for('index'))

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        usuario = Usuario.realizar_login(email, senha)
        if usuario and usuario.check_senha(senha):
            session['user_id'] = usuario.id
            return redirect(url_for('index'))
        else:
            return 'Credenciais inválidas'
    return render_template('login.html')

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        if senha != confirmar_senha:
            return 'Os campos de senha não coincidem!', 404
        
        novo_usuario = Usuario(email=email, nome=nome, senha=senha)
        Usuario.realizar_cadastro(novo_usuario)
        return redirect(url_for('login'))

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

    novo_produto = Produto(titulo, autor, genero, sinopse, imagem)

    Produto.adicionar_produto(novo_produto)

    return render_template('adicao.html')

@app.route('/remocao', methods=["GET"])
def remocao():
    return render_template('remocao.html')

@app.route('/remover', methods=["POST"])
def remover():
    produto_id = request.form['produto_id']
    try:
        produto_id = int(produto_id)
    except ValueError:
        return 'ID do produto inválido', 400

    Produto.remover_produto(produto_id)

    return render_template('remocao.html')

@app.route('/produto/<int:produto_id>')
def produto(produto_id):
    produto = Produto.query.get_or_404(produto_id)
    return render_template('produto.html', produto=produto)

if __name__ == '__main__':
    app.run(debug=True)