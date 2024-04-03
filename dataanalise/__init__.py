import pandas as pd
import plotly.express as px


#https://www3.bcb.gov.br/sgspub/localizarseries/localizarSeries.do?method=prepararTelaLocalizarSeries
def consulta_bc(codigo_bcb):
  url = 'http://api.bcb.gov.br/dados/serie/bcdata.sgs.{}/dados?formato=json'.format(codigo_bcb)
  df = pd.read_json(url)
  df['data'] = pd.to_datetime(df['data'], dayfirst=True)
  df.set_index('data', inplace=True)
  return df

def converterIndicadorCodigo(indicador):
    if indicador == 'PB':
        return '12743'

    elif indicador == 'AL':
        return '12745'

    elif indicador == 'BA':
        return '12991'

    elif indicador == 'CE':
        return '13010'

    elif indicador == 'RN':
        return '12744'

    elif indicador == 'PE':
        return '28268'

    elif indicador == 'Consumo de energia elétrica – residencial – região Nordeste':
        return '1413'

    elif indicador == 'Consumo de energia elétrica – residencial – Região Sul':
        return '1418'

    elif indicador == 'Consumo de energia elétrica – residencial – região Norte':
        return '1408'



def correlacionar_indicadores(indicador1, indicador2):
    code1 = converterIndicadorCodigo(indicador1)
    code2 = converterIndicadorCodigo(indicador2)

    dados1 = consulta_bc(code1)
    dados2 = consulta_bc(code2)
    dados1 = dados1[dados1.index >= '2014-01-01']
    #dados1 = dados1.resample('1m').mean()

    dados2 = dados2[dados2.index >= '2014-01-01']
    #dados2 = dados2.resample('1m').mean()
    #dados2.drop(dados2.index[-1], inplace=True)

    geral = pd.concat([dados1, dados2], axis=1)
    correlacao = (geral,geral.corr().values[0][1])

    return correlacao





import plotly.graph_objects as go

def gerarGrafCorrInd(graficodados):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name=graficodados.columns[0],
        x=graficodados.index,
        y=graficodados[graficodados.columns[0]],  # Dados para o eixo y,
        mode='lines',  # Tipo de gráfico: linhas,
        line=dict(color='blue')  # Altera a cor das linhas

    ))
    fig.update_layout(
        autosize=True,
        width=900,
        height=500
    )
    fig.add_trace(go.Scatter(
        name=graficodados.columns[1],
        x=graficodados.index,
        y=graficodados[graficodados.columns[1]],  # Dados para o eixo y,
        mode='lines',  # Tipo de gráfico: linhas,
        line=dict(color='red'),  # Altera a cor das linhas
        legendgroup='Cotação'
    ))
    return fig



