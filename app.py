from flask import Flask, render_template, request, redirect, url_for, session, flash
#import src.entidades.db_operations as OperationsDB
from src.entidades.produto import Produto
from src.entidades.usuario import Usuario
from src.entidades.db_operations import db

app = Flask(__name__)
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

@app.route('/buscar', methods=['GET'])
def buscar():
    pesquisa = request.args.get('pesquisa', '')  # Obtenha o termo de pesquisa da query string
    produtos = Produto.query.filter(Produto.titulo.ilike(f'%{pesquisa}%')).all()  # Consulta para buscar produtos correspondentes

    # Renderize o template com os resultados da pesquisa
    return render_template('index.html', produtos=produtos)

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
            flash('Credencias inválidas!', 'error')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == 'POST':
        email = request.form['email']
        nome = request.form['nome']
        senha = request.form['senha']
        confirmar_senha = request.form['confirmar_senha']

        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('Este e-mail já está cadastrado.', 'error')
            return redirect(url_for('cadastro'))

        if senha != confirmar_senha:
            flash('Os campos de senha precisam coincidir!', 'error')
            return render_template('cadastro.html')
        
        novo_usuario = Usuario(email=email, nome=nome, senha=senha)
        Usuario.realizar_cadastro(novo_usuario)
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/adicao', methods=['GET'])
def adicao():
    if 'user_id' in session:
        usuario_id = session['user_id']
        usuario = Usuario.query.get(usuario_id)
        return render_template('adicao.html', usuario=usuario)

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
    if 'user_id' in session:
        usuario_id = session['user_id']
        usuario = Usuario.query.get(usuario_id)
        return render_template('remocao.html', usuario=usuario)

    return render_template('remocao.html')

@app.route('/remover', methods=["POST"])
def remover():
    produto_id = request.form['produto_id']
    try:
        produto_id = int(produto_id)
    except ValueError:
        flash('Insira um ID de produto valido', 'error')
        return render_template('remocao.html')
    
    produto_existente = Produto.query.get(produto_id)
    if not produto_existente:
        flash('Produto inexistente', 'error')
        return render_template('remocao.html')
    
    Produto.remover_produto(produto_id)

    return render_template('remocao.html')

@app.route('/produto/<int:produto_id>', methods=['GET'])
def produto(produto_id):
    produto = Produto.query.get(produto_id)
    
    if 'user_id' in session:
        usuario_id = session['user_id']
        usuario = Usuario.query.get(usuario_id)

        esta_na_biblioteca = produto in usuario.minha_biblioteca
    else:
        esta_na_biblioteca = False

    return render_template('produto.html', produto=produto, esta_na_biblioteca=esta_na_biblioteca)

@app.route('/minha_biblioteca', methods=["GET", "POST"])
def minha_biblioteca():
    if 'user_id' in session:
        usuario = Usuario.query.filter_by(id=session['user_id']).first()
        meus_produtos = usuario.minha_biblioteca
        return render_template('minha_biblioteca.html', meus_produtos=meus_produtos)
    return render_template('minha_biblioteca.html')

@app.route('/adicionar_biblioteca/<int:produto_id>', methods=['POST'])
def adicionar_a_biblioteca(produto_id):
    produto = Produto.query.get(produto_id)
    if 'user_id' in session:
        usuario_id = session['user_id']
        usuario = Usuario.query.get(usuario_id)

        usuario.adicionar_a_biblioteca(produto)

    return redirect(url_for('produto', produto_id=produto_id))

@app.route('/remover_da_biblioteca/<int:produto_id>', methods=['POST'])
def remover_da_biblioteca(produto_id):
    produto = Produto.query.get(produto_id)
    if 'user_id' in session:
        usuario_id = session['user_id']
        usuario = Usuario.query.get(usuario_id)

        usuario.remover_da_biblioteca(produto)
    return redirect(url_for('produto', produto_id=produto_id))

if __name__ == '__main__':
    app.run(debug=True)