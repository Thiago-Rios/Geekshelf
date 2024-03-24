import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from src.entidades.produto import Produto
from PIL import Image
from io import BytesIO
from app import app
from src.entidades.db_operations import db

class TestProduto(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

            produto1 = Produto(titulo="Livro 1", autor="Autor 1", genero="Ficção", sinopse="Sinopse do livro 1", imagem=None)
            produto2 = Produto(titulo="Livro 2", autor="Autor 2", genero="Não-ficção", sinopse="Sinopse do livro 2", imagem=None)
            db.session.add(produto1)
            db.session.add(produto2)
            db.session.commit()

            self.produto1_id = produto1.id
            self.produto2_id = produto2.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()    

    def test_adicionando_novo_produto(self):
        # Criar uma instância de Produto
        with app.app_context():
            titulo = "Livro Teste"
            autor = "Autor Teste"
            genero = "Ficção"
            sinopse = "Sinopse do livro de teste"
            imagem = BytesIO()
            imagem_png = Image.new('RGB', (100, 100), color='red')
            imagem_png.save(imagem, format='PNG')
            imagem.seek(0)

            produto_adicionado = Produto(titulo, autor, genero, sinopse, imagem)

            Produto.adicionar_produto(produto_adicionado)

            produto_adicionado = Produto.query.filter_by(titulo=titulo).first()
            self.assertIsNotNone(produto_adicionado)
            self.assertEqual(produto_adicionado.titulo, titulo)
            self.assertEqual(produto_adicionado.autor, autor)
            self.assertEqual(produto_adicionado.genero, genero)
            self.assertEqual(produto_adicionado.sinopse, sinopse)

    def test_remover_produto(self):
        with app.app_context():
            Produto.remover_produto(self.produto1_id)

            produto_removido = Produto.query.get(self.produto1_id)
            self.assertIsNone(produto_removido)

            produto_restante = Produto.query.get(self.produto2_id)
            self.assertIsNotNone(produto_restante)

if __name__ == '__main__':
    unittest.main()