from PIL import Image
from io import BytesIO
from app import db

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(60), nullable=False)
    autor = db.Column(db.String(60), nullable=False)
    genero = db.Column(db.String(60), nullable=False)
    sinopse = db.Column(db.Text, nullable=False)
    imagem = db.Column(db.LargeBinary, nullable=True)

    @staticmethod
    def adicionar_produto(titulo, autor, genero, sinopse, imagem):
        # Converter imagem para formato PNG
        imagem_png = Image.open(imagem)
        imagem_png = imagem_png.convert('RGB')

        # Salvar a imagem convertida em um buffer de bytes
        imagem_buffer = BytesIO()
        imagem_png.save(imagem_buffer, format='PNG')
        imagem_buffer.seek(0)

        # Criar instância do Produto
        novo_produto = Produto(titulo=titulo, autor=autor, genero=genero, sinopse=sinopse, imagem=imagem_buffer.read())

        # Adicionar e commit no banco de dados
        db.session.add(novo_produto)
        db.session.commit()

        return novo_produto