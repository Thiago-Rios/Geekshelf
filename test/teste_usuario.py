import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from src.entidades.produto import Produto
from src.entidades.usuario import Usuario
from app import app
from src.entidades.db_operations import db

class TestUsuario(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()
        with app.test_request_context():
            db.create_all()

            self.email = 'exemplo@teste.com'
            self.senha = 'senha_segura'
            self.novo_usuario = Usuario(nome='Exemplo', email=self.email)
            self.novo_usuario.set_senha(self.senha)
            self.produto1 = Produto(titulo="Livro 1", autor="Autor 1", genero="Ficção", sinopse="Sinopse do livro 1", imagem=None)
            db.session.add(self.novo_usuario)
            db.session.add(self.produto1)
            db.session.commit()

    def tearDown(self):
        with app.test_request_context():
            db.session.remove()
            db.drop_all()
            self.ctx.pop()

    def test_realizar_login(self):
        with app.test_request_context():
            usuario = Usuario.realizar_login(self.email, self.senha)
            self.assertIsNotNone(usuario)

            usuario_invalido = Usuario.realizar_login('email_invalido@teste.com', 'senha_incorreta')
            self.assertIsNone(usuario_invalido)

    def test_realizar_cadastro(self):
        with app.test_request_context():
            novo_usuario = Usuario(nome='Novo Usuario', email='novo@teste.com', senha='senha_segura')
            Usuario.realizar_cadastro(novo_usuario)

            usuario_cadastrado = Usuario.query.filter_by(email='novo@teste.com').first()
            self.assertIsNotNone(usuario_cadastrado)

    def test_realizar_logout(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1
        Usuario.realizar_logout(sess)
        self.assertNotIn('user_id', sess)

    def test_adicionar_a_biblioteca(self):
        with app.test_request_context():
            self.novo_usuario.adicionar_a_biblioteca(self.produto1)
            self.assertTrue(self.produto1 in self.novo_usuario.minha_biblioteca)

    def test_remover_da_biblioteca(self):
        with app.test_request_context():
            self.novo_usuario.remover_da_biblioteca(self.produto1)
            self.assertFalse(self.produto1 in self.novo_usuario.minha_biblioteca)

if __name__ == '__main__':
    unittest.main()