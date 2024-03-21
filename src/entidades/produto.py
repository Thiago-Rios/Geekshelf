# import os
# import sys
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from PIL import Image
from io import BytesIO
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flqprwqe:3n0mkft13qCefWX3ZLDx8313X6LdBzX5@kesavan.db.elephantsql.com/flqprwqe'
db = SQLAlchemy(app)

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(60), nullable=False)
    autor = db.Column(db.String(60), nullable=False)
    genero = db.Column(db.String(60), nullable=False)
    sinopse = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.LargeBinary, nullable=True)
    avaliacao = db.Column(db.Integer, nullable=True)

    def __init__(self, titulo, autor, genero, sinopse, imagem):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero
        self.sinopse = sinopse
        self.imagem = imagem

    @staticmethod
    def adicionar_produto(titulo, autor, genero, sinopse, imagem):
        imagem_png = Image.open(imagem)
        imagem_png = imagem_png.convert('RGB')
        imagem_buffer = BytesIO()
        imagem_png.save(imagem_buffer, format='PNG')
        imagem_buffer = imagem_buffer.getvalue()

        novo_produto = Produto(titulo=titulo, autor=autor, genero=genero, sinopse=sinopse, imagem=imagem_buffer)
        
        return novo_produto