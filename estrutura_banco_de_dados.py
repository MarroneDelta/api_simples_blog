from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext  # Para criptografar a senha de forma segura
from werkzeug.security import generate_password_hash


#Criar um API- Flask
app = Flask(__name__)
#Criar um instancia de sqlchemy
app.config['SECRET_KEY'] = 'FDS3252!AHG%#A'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:[YOUR_PASSWORD]@db.ftngxdgwdjpynhoqemsl.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db: SQLAlchemy
#Definir estrutura da tabela posdtagem
class Postagem(db.Model):
    __tablename__ = 'postagem'
    id_postagem = db.Column(db.Integer,primary_key=True)
    titulo = db.Column(db.String)
    id_autor = db.Column(db.Integer,db.ForeignKey('autor.id_autor'))

class Autor(db.Model):
    __tablename__ = 'autor'
    #id_autor
    id_autor = db.Column(db.Integer,primary_key=True)
    #nome_autor
    nome_autor= db.Column(db.String)
    #email_autor
    email_autor=db.Column(db.String)
    #senha_autor
    senha=db.Column(db.String)
    #admin
    admin = db.Column(db.Boolean)

    #Relaçao com a tabela 
    postagens = db.relationship('Postagem')

# Executar o comando para criar Bando de dados
# definir estrutura da tabela autor
# Todo autor: id_autor, nome,email,senha,admin,postagens
def inicializa_banco():
    with app.app_context():
        db.drop_all()
        db.create_all()

        #Criar usuarios administrativos

        autor = Autor(nome_autor='Marco',

            email_autor='dalkelevadores@gmail.com',
            senha='12345',
            admin=True )
        db.session.add(autor)
        db.session.commit()


if __name__ == '__main__':
    inicializa_banco()




