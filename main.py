from flask import *
import dao
import dataanalise as da
import plotly.express as px
import plotly.graph_objects as go



app = Flask(__name__)


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

        return render_template('correlacaoResultado.html', plot=fig.to_html())

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

            return render_template('correlacaoResultado.html', plot=fig.to_html())




@app.route('/cadastrarusuario', methods=['GET', 'POST'])
def redirecionar_cadastro_user():
    if request.method == 'GET':
        return render_template('cadastrarusuario.html')
    elif request.method == 'POST':
        login = str(request.form.get('nome'))
        senha = str(request.form.get('senha'))

        if dao.inserirDB(login, senha, dao.conectardb()):
            return render_template('index2.html')
        else:
            texto = 'e-mail já cadastrado'
            return render_template('index2.html', msg=texto)


@app.route('/login', methods=['POST'])
def cadastrar_usuario():
    nome = str(request.form.get('nome'))
    senha = str(request.form.get('senha'))

    if dao.verificarlogin(nome, senha, dao.conectardb()):
        return render_template('menu.html')
    else:
        return render_template('index2.html')


@app.route('/grafvioleciapib', methods=['POST', 'GET'])
def gerarGrafViolenciaPib():
    if request.method == 'POST':
        filtro = int(request.form.get('valor'))
    else:
        filtro = 10

    dados = da.lerdados()
    dados.drop(dados.sort_values(by=['cvli'], ascending=False).head(3).index, inplace=True)
    dados.drop(dados.sort_values(by=['rendapercapita'], ascending=False).head(filtro).index, inplace=True)
    dados.drop(dados.sort_values(by=['rendapercapita'], ascending=True).head(2).index, inplace=True)

    fig = px.scatter(dados, x='rendapercapita', y='cvli', hover_data=['municipio'])
    return render_template('grafviolenciapib.html', plot=fig.to_html())


@app.route('/grafcorrelacao')
def gerarGrafCorrelacao():
    dados = da.lerdados()
    fig2 = da.exibirmapacorrelacoes(dados)

    return render_template('grafcorrelacao.html', mapa=fig2.to_html())


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/')
def motormanda():
    return render_template('index2.html')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
