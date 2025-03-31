#Nosso primeira API
#FLAS

from flask import Flask, jsonify, request , make_response
from estrutura_banco_de_dados import Autor,Postagem,app,db
import json
import jwt
from datetime import datetime,timedelta
from functools import wraps

def token_obrigatorio(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        #verificar se o token foi enviado com a requisiçao
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        
        if not token:
            return jsonify({'Mensagem': 'Token nao foi incluido!'},401)
        # Se temos um token,verificar se esta correto junto ao banco de dados;
        try:
            resultado = jwt.decode(token,app.config['SECRET_KEY'], algorithms=["HS256"])
            autor = Autor.query.filter_by(id_autor=resultado['id_autor']).first()
        except:
            return jsonify({'Mensagem':'Token é invalido'},401)
        return f(autor,*args, **kwargs)
    return decorated


# Definiçaõ da Rota Padrão : Basicamente pode ser entendida como 
#Nosso GET -


@app.route('/login')
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('login invalida',401,{'WWW-Autenticate': 'Basic realm = "Login Obrigatorio"'})
    usuario = Autor.query.filter_by(nome_autor=auth.username).first()
    if not usuario:
        return make_response('login invalida',401,{'WWW-Autenticate': 'Basic realm = "Login Obrigatorio"'})
    if auth.password == usuario.senha:
        token = jwt.encode({'id_autor':usuario.id_autor,
        'exp':datetime.utcnow() + 
        timedelta(minutes = 30)}, 
        app.config['SECRET_KEY'])
        return jsonify({'token': token})
    return make_response('login invalida',401,{'WWW-Autenticate': 'Basic realm = "Login Obrigatorio"'})


@app.route('/')
@token_obrigatorio
def obter_postagem(autor):

    postagens = Postagem.query.all()
    lista_de_postagens = [
        {'id_postagem': p.id_postagem, 'titulo': p.titulo, 'id_autor': p.id_autor}
        for p in postagens
    ]
    return jsonify(lista_de_postagens)


#GET POR INDICE= http://localhost:5000/postagem/1

@app.route('/postagem/<int:indice>', methods=['GET'])
@token_obrigatorio
def obter_postagem_por_indice(autor, indice):
    return jsonify(postagens[indice])

######Criar uma noca Postagem - POST -
#  http://localhost:7777/postagem


@app.route('/postagem',methods=['POST'])

def nova_postagem(autor):
    postagem=request.get_json()
    postagens.append(postagem)

    return jsonify(postagem,200)

#### ALterar uma Postagem ja existente...abs
## PUT -

@app.route('/postagem/<int:indice>', methods=['PUT'])
@token_obrigatorio
def alterar_postagem(autor,indice):
    postagem_alterada = request.get_json()
    postagens[indice].update(postagem_alterada)

    return jsonify(postagens[indice], 200)

#### Excluir 
##Delete--

@app.route('/postagem/<int:indice>', methods=['DELETE'])
@token_obrigatorio
def apagar_postagens(autor,indice):
    try:
        if postagens[indice] is not None:
            del postagens[indice]
            return jsonify(f'Foi excluido a postagem {postagens[indice]}', 200)
    except:
        return jsonify('Nao foi possivel excluir a Postagem' ,404)




@app.route('/autores')
@token_obrigatorio
def obter_autores(autor):
    autores = Autor.query.all()
    lista_de_autores= []
    for autor in autores:
        autor_atual = {}
        autor_atual['id_autor'] = autor.id_autor
        autor_atual['nome_autor']= autor.nome_autor
        autor_atual['email_autor'] = autor.email_autor
        autor_atual['admin'] =  autor.admin
       # admin=novo_autor.get('admin', False) 
        lista_de_autores.append(autor_atual)
    return jsonify({'autores': lista_de_autores})


@app.route('/autores/<int:id_autor>', methods=['GET'])
@token_obrigatorio
def obter_autor_por_id(autor,id_autor):
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    if not autor:
        return jsonify(f'Nao existe o {autor} selecionado')
    autor_atual = {}
    autor_atual['id_autor'] = autor.id_autor
    autor_atual['nome_autor']= autor.nome_autor
    autor_atual['email_autor'] = autor.email_autor

    return jsonify({'autor': autor_atual})


@app.route('/autores' , methods=['POST'])
@token_obrigatorio
def novo_autor(autor):
    novo_autor= request.get_json()
    autor=Autor(
        nome_autor=novo_autor['nome_autor'],
        senha=novo_autor['senha'],
        email_autor=novo_autor['email_autor'])
    db.session.add(autor)
    db.session.commit()

    return jsonify({'mensagem':f'O novo autor {autor.nome_autor} foi add,com sucesso'}), 201


@app.route('/autores/<int:id_autor>', methods=['PUT'])
@token_obrigatorio
def alterar_autor(autor,id_autor):
    usuario_a_alterar=request.get_json()
    autor = Autor.query.filter_by(id_autor=id_autor).first()
    
    if not autor:
        return jsonify({'mensagem': 'Este usuario não foi Encontrado'})
    
        
    try:
         if usuario_a_alterar['nome_autor']:
            autor.nome_autor = usuario_a_alterar['nome_autor']
    except:
        pass
    try:
        if usuario_a_alterar['email_autor']:
            autor.email_autor = usuario_a_alterar['email_autor']
    except:
        pass

    try:
        
        if usuario_a_alterar['senha']:
            autor.senha = usuario_a_alterar['senha']
    except:
        pass
    
    db.session.commit()
    return jsonify({'mensagem': 'Usuario alterado com sucesso'}), 200

    

@app.route('/autores/<int:id_autor>',methods=['DELETE'])
@token_obrigatorio
def excluir_autor(autor,id_autor):
    
    autor_existente=Autor.query.filter_by(id_autor=id_autor).first()
    
    if not autor_existente:
        return jsonify({'mensagem': 'Autor não encontrado'})
    
    db.session.delete(autor_existente)
    db.session.commit()

    return jsonify({'Mensagem': f'Autor : {autor_existente.nome_autor} foi excluido com sucesso !'})




app.run(port=5000,host='localhost',debug=True)
