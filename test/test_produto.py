import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.entidades.produto import Produto
from PIL import Image
from io import BytesIO
from app import app, db

class TestProduto(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

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

            produto_adicionado = Produto.adicionar_produto(titulo, autor, genero, sinopse, imagem)

            self.assertIsNotNone(produto_adicionado)
            self.assertEqual(produto_adicionado.titulo, titulo)
            self.assertEqual(produto_adicionado.autor, autor)
            self.assertEqual(produto_adicionado.genero, genero)
            self.assertEqual(produto_adicionado.sinopse, sinopse)
            self.assertIsNotNone(produto_adicionado.imagem)

if __name__ == '__main__':
    unittest.main()