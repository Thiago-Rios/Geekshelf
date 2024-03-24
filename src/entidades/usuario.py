import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.entidades.db_operations import db
from flask import session, redirect, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    senha = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Usuario %r>' % self.email

    def set_senha(self, senha):
        self.senha = generate_password_hash(senha)

    def check_senha(self, senha):
        return check_password_hash(self.senha, senha)
    
    @staticmethod
    def realizar_login(email, senha):
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and usuario.check_senha(senha):
            return usuario
        return None
        
    @staticmethod
    def realizar_cadastro(novo_usuario):
        usuario = Usuario(nome=novo_usuario.nome, email=novo_usuario.email)
        usuario.set_senha(novo_usuario.senha)
        db.session.add(usuario)
        db.session.commit()

    @staticmethod
    def realizar_logout(sess):
        sess.pop('user_id', None)
        
    