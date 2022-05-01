# O que e o Flask?

# E um microframework capaz de colocar uma aplicacao no ar de forma rapida e eficiente,
# porque contem apenas o essencial para ser executado e conta com a capacidade de ser
# integrado por outras ferramentas caso precise de mais recursos.

# Principais Caracteristicas

# - Simplicidade;
# - Rapidez;
# - Eficiencia;

# Codigo de ativacao do virtual env: .\venv\Scripts\activate
# Codigo de desativacao do virtual env: deactivate

# Referencia a biblioteca e em seguida importa a funcao desejada
# Caso esteja utilizando pela primeira vez, tambem sera necessario baixar a biblioteca
# via pip install porque ela nao e uma biblioteca padrao python
# render_template: renderiza a pagina html
# request: recebe valores digitados pelo usuario no front-end
# redirect: redireciona o usuario para uma pagina definida
# session: retem informacao por mais de um ciclo de acesso nos cookies do navegador
# flash: permite mostrar mensagens ao usuario
# url_for: na hipotese de alteracao e de que haja diversas referencias a uma mesma rota,
# pode-se adotar essa funcao para que altere-as com facilidade
from flask import Flask, flash, render_template, request, redirect, session, flash, url_for

# Criando variavel onde sera colocada a aplicacao. O __name__ faz referencia ao proprio
# arquivo, garantindo que a aplicacao rode.
app = Flask(__name__)


# adicionando uma camada de criptografia a app
app.secret_key = 'luciano'

# Para apresentar qualquer informacao no site, e necessario criar uma rota, nomeando-a
# Toda vez que se cria uma nova rota, e necessario criar uma funcao que define o que existe
# nela rota
# @app.route('/inicio')
# def ola():
#     return '<h1>Olá mundo!</h1>'

# Script para renderizar o arquivo html, onde se pode criar diretiva de duplo couchete
# {{ <nome_variavel> }}, que serve para se inserir codigo python no html e onde se le variavel e
# por onde pode ser inserido as informacoes desejas.

# Uma forma de criar variaveis no html e atribuir valores pelo python/servidor
# @app.route('/inicio')
# def ola():
#    jogo1 = 'God of War'
#    jogo2 = 'Skyrim'
#    jogo3 = 'Valorant'
#    return render_template('lista.html', 
#                            titulo = 'Jogos', 
#                            jogo1 = jogo1, 
#                            jogo2 = jogo2,
#                            jogo3 = jogo3)


# Cria classe para instanciar objetos
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


# Valores Globais
# instanciando objetos na classe
jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
# adicionado objetos em lista
lista = [jogo1, jogo2, jogo3]


# Cria classe para instanciar usuarios
class Usuario:
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha


# Valores Globais
# instanciando objetos na classe
usuario1 = Usuario('Luciano', 'Luck', 'senha_mestra_*')
usuario2 = Usuario('Rukia', 'Rukinha', 'senha2')
usuario3 = Usuario('Juju', 'Jujubinha', 'senha3')
# adicionado objetos em dicionario
usuarios = {
    usuario1.nickname : usuario1,
    usuario2.nickname : usuario2,
    usuario3.nickname : usuario3
}


# Script que renderiza html com estrutura de for. Nesse cado, e necessario se usar
# no html uma nova estrutura constituida pelo inicio em {% for <variavel_provisoria> in <lista> %}
# e finalizado em {% endfor %}
# @app.route('/inicio')
# def ola():
#     # instanciando objetos na classe
#     jogo1 = Jogo('Tetris', 'Puzzle', 'Atari')
#     jogo2 = Jogo('God of War', 'Rack n Slash', 'PS2')
#     jogo3 = Jogo('Mortal Kombat', 'Luta', 'PS2')
#     # adicionado objetos em lista
#     lista = [jogo1, jogo2, jogo3]
#     # renderizando html e atribuindo valores as variaveis
#     return render_template('lista.html', 
#                             titulo = 'Jogos', 
#                             jogos = lista)

@app.route('/')
def index():
    # renderizando html e atribuindo valores as variaveis
    return render_template('lista.html', 
                            titulo = 'Jogos', 
                            jogos = lista)


# Rota para inserir novos jogos pela aplicacao
@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # return redirect('/login?proxima=novo') # redireciona o usuario para pagina especifica usando query string, apos credenciais corretas, enviando valor para rota login
        return redirect(url_for('login', proxima = url_for('novo')))
    return render_template('novo.html', titulo = 'Novo Jogo')


# Rota (de processamento*) que insere informacoes recebidas do form no servidor
@app.route('/criar', methods=['POST', ])
def criar():
    # capturando nomes digitados pelo usuario no front-end
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    # criando objeto
    jogo = Jogo(nome, categoria, console)
    # adicionando na lista
    lista.append(jogo)
    # redireciona o usuario para a pagina definida na funcao
    return redirect(url_for('index')) # render_template('lista.html', titulo = 'Jogos', jogos = lista)


# Rota para criar novos logins
@app.route('/login')
def login():
    proxima = request.args.get('proxima') #captura informacao enviada pela rota /novo
    return render_template('login.html', proxima = proxima)


# Rota (de processamento*) para acesso do usuario aos servicos da pagina
@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ', logado com sucesso!') # permite mostrar uma mensagem em caso de sucesso
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
        else:
            flash('Usuario nao logado.')
            return redirect(url_for('login'))
    # if 'senha_mestra_*' == request.form['senha']:
    #     session['usuario_logado'] = request.form['usuario'] # armazena o valor em cookie do navegador
    #     flash(session['usuario_logado'] + ', logado com sucesso!') # permite mostrar uma mensagem em caso de sucesso
    #     proxima_pagina = request.form['proxima']
    #     # return redirect('/{}'.format(proxima_pagina))
    #     return redirect(proxima_pagina)
    # else:
    #     flash('Usuario nao logado.')
    #     return redirect(url_for('login'))


# Rota para efetuar o logout do usuario
@app.route('/logout')
def logout():
    session['usuario_logado'] = None # atribuindo valor none para que se "esqueca" a informacao
    flash('Logout efetuado com sucesso.') # mensagem que informa que a operacao ocorreu com sucesso
    return redirect(url_for('index'))

# Para que a aplicacao possa ser executada.
# O parametro debug=True permite que o servidor seja executado sempre, sem a necessidade
# religa-lo sempre
app.run(debug=True)