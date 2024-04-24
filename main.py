from flask import *
import pandas as pd
import dao
import dataanalise as da
import plotly.express as px
import plotly.graph_objects as go



app = Flask(__name__)

@app.route('/')
def motormanda():
    return render_template('index2.html')


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/login', methods=['POST'])
def cadastrar_usuario():
    nome = str(request.form.get('nome'))
    senha = str(request.form.get('senha'))

    if dao.verificarlogin(nome, senha, dao.conectardb()):
        return render_template('menu.html')
    else:
        return render_template('index2.html')


@app.route('/cadastrarusuario', methods=['GET', 'POST'])
def redirecionar_cadastro_user():
    if request.method == 'GET':
        return render_template('cadastrarusuario.html')
    elif request.method == 'POST':
        login = str(request.form.get('nome'))
        senha = str(request.form.get('senha'))

        if dao.verificarlogin(login, senha, dao.conectardb()):
            return render_template('index2.html')
        else:
            texto = 'e-mail já cadastrado'
            return render_template('index2.html', msg=texto)




@app.route('/correlacaoindicadores', methods=['GET', 'POST'])
def calcular_correlacao_individual():
    if request.method == 'GET':
        return render_template('escolherindicadores.html')
    else:
        ind1 = request.form.get('indicador1')
        ind2 = request.form.get('indicador2')
        dados, correlacao = da.correlacionar_indicadores(ind1, ind2)
        dados.columns = [ind1, ind2]
        fig = da.gerarGrafCorrInd(dados)


        dao.correlacionar_indicadores_e_inserir_bd(ind1, ind2, dao.conectardb())
        return render_template('correlacaoResultado.html', valor=correlacao, plot=fig.to_html())

        # return f'<h1>{correlacao}</h1>'

@app.route('/consumoenergia', methods=['GET', 'POST'])
def gerar_graf_consumo_energia():
        if request.method == 'GET':
            return render_template('consumoenergia.html')
        else:
            ind1 = request.form.get('indicador1')
            ind2 = request.form.get('indicador2')
            dados, correlacao = da.correlacionar_indicadores(ind1, ind2)
            dados.columns = [ind1, ind2]
            fig = da.gerarGrafCorrInd(dados)

            dao.correlacionar_indicadores_e_inserir_bd(ind1, ind2, dao.conectardb())

            return render_template('correlacaoResultado.html', valor=correlacao, plot=fig.to_html())


if __name__ == '__main__':
    app.run(debug=True, port=5001)
