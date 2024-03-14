import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from app import app, db
from PIL import Image
from io import BytesIO
from src.entidades.produto import Produto

class TestDB(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()

    def test_conexao_bd(self):
        with app.app_context():
            self.assertIsNotNone(db.engine)

    def test_criacao_tabela(self):
        with app.app_context():
            meta = db.metadata
            self.assertTrue(Produto.__tablename__ in meta.tables)

    def test_criacao_entidade_db(self):
        with app.app_context():
            titulo = "Livro Teste"
            autor = "Autor Teste"
            genero = "Ficção"
            sinopse = "Sinopse do livro de teste"
            imagem = BytesIO()
            imagem_png = Image.new('RGB', (100, 100), color='red')
            imagem_png.save(imagem, format='PNG')
            imagem_bytes = imagem.getvalue()

            produto = Produto(titulo, autor, genero, sinopse, imagem_bytes)
            db.session.add(produto)
            db.session.commit()

            produto_recuperado = Produto.query.filter_by(titulo='Livro Teste').first()
            self.assertIsNotNone(produto_recuperado)
            self.assertEqual(produto.titulo, titulo)
            self.assertEqual(produto.autor, autor)
            self.assertEqual(produto.genero, genero)
            self.assertEqual(produto.sinopse, sinopse)
            self.assertIsNotNone(produto.imagem)

if __name__ == '__main__':
    unittest.main()
