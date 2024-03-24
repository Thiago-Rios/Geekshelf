import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from PIL import Image
from io import BytesIO
from src.entidades.db_operations import db

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
    def adicionar_produto(produto):
        imagem_png = Image.open(produto.imagem)
        imagem_png = imagem_png.convert('RGB')
        imagem_buffer = BytesIO()
        imagem_png.save(imagem_buffer, format='PNG')
        imagem_buffer = imagem_buffer.getvalue()

        novo_produto = Produto(titulo=produto.titulo, autor=produto.autor, genero=produto.genero, sinopse=produto.sinopse, imagem=imagem_buffer)
        
        db.session.add(novo_produto)
        db.session.commit()
    
    @staticmethod
    def remover_produto(produto_id):
        produto = Produto.query.get(produto_id)

        db.session.delete(produto)
        db.session.commit()


        
