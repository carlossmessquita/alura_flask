# Trazendo Flask e outras funções necessárias:
from flask import Flask, render_template, request, redirect, session, flash, url_for
from classes import Jogo, Usuario

# Instanciando jogos manualmente:
jogo1 = Jogo('God of War', 'Rack n Slash', 'PlayStation')
jogo2 = Jogo('God of War II', 'Rack n Slash', 'PlayStation 2')
jogo3 = Jogo('God of War III', 'Rack n Slash', 'PlayStation 3')
jogo4 = Jogo('Mortal Kombat 11', 'Luta', 'PlayStation 4')

lista = [jogo1, jogo2, jogo3, jogo4]

# Instanciando jogos manualmente:
user = Usuario('Carlos', 'cvsm', 'Mesquito')
user_dois = Usuario('Vitor', 'msqt', 'Da Silva')

usuarios = {
    user.nickname : user,
    user_dois.nickname : user_dois
}


# Criando instância Flask:
app = Flask(__name__)
app.secret_key = 'msqt'


# Definindo rotas:
@app.route('/')
def index():
    return render_template('index.html', titulo='Jogos', jogos=lista)


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima, titulo='Faça Seu Login')


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(f'{usuario.nickname} logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário ou Senha incorreto(s)!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        flash('Realize login para cadastrar novo jogo!')
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        return render_template('newgame.html', titulo='Novo Jogo')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    flash(f'Jogo {nome} cadastrado com sucesso!')
    return redirect(url_for('index'))


# Rodando aplicação:
app.run(host='0.0.0.0', port=8080, debug=True)
