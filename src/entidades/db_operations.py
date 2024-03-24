from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db = SQLAlchemy()

class OperationsDB():

    def get_all_products(self, db):
        query = text('SELECT * FROM produtos')
        result = db.session.execute(query)
        produtos = result.fetchall()
        return produtos

    