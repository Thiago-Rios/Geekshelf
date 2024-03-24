import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest
from src.entidades.usuario import Usuario
from app import app
from src.entidades.db_operations import db

class TestUsuario(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

            self.email = 'exemplo@teste.com'
            self.senha = 'senha_segura'
            novo_usuario = Usuario(nome='Exemplo', email=self.email)
            novo_usuario.set_senha(self.senha)
            db.session.add(novo_usuario)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_realizar_login(self):
        with app.app_context():
            usuario = Usuario.realizar_login(self.email, self.senha)
            self.assertIsNotNone(usuario)

            usuario_invalido = Usuario.realizar_login('email_invalido@teste.com', 'senha_incorreta')
            self.assertIsNone(usuario_invalido)

    def test_realizar_cadastro(self):
        with app.app_context():
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

if __name__ == '__main__':
    unittest.main()