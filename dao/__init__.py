import pandas as pd
import psycopg2

from dataanalise import converterIndicadorCodigo, consulta_bc


def conectardb():
    con = psycopg2.connect(
        host='localhost',
        database='projetoflask',
        user='postgres',
        password='12345'
    )
    return con

def inseriruser(login, senha, conexao):
    cur = conexao.cursor()
    exito = False
    try:
        sql = f"INSERT INTO usuarios (login, senha) VALUES ('{login}', '{senha}' )"
        cur.execute(sql)
    except psycopg2.IntegrityError:
        conexao.rollback()
        exito = False
    else:
        conexao.commit()
        exito = True

    conexao.close()
    return exito

def verificarlogin(nome, senha, conexao):

    cur = conexao.cursor()
    cur.execute(f"SELECT count(*) FROM usuarios WHERE login = '{nome}' AND senha = '{senha}'")
    recset = cur.fetchall()
    conexao.close()
    if recset[0][0] == 1:
        return True
    else:
        return False

def listarUsuarios(conexao):
    cur = conexao.cursor()
    cur.execute('select * from usuarios')
    recset = cur.fetchall()
    conexao.close()

    return recset

def correlacionar_indicadores_e_inserir_bd(indicador1, indicador2, conexao):
    code1 = converterIndicadorCodigo(indicador1)
    code2 = converterIndicadorCodigo(indicador2)

    dados1 = consulta_bc(code1)
    dados2 = consulta_bc(code2)
    dados1 = dados1[dados1.index >= '2014-01-01']
    dados2 = dados2[dados2.index >= '2014-01-01']

    geral = pd.concat([dados1, dados2], axis=1)
    correlacao_valor = geral.corr().values[0][1]


    cur = conexao.cursor()
    try:
        sql = f"INSERT INTO correlacoes (indicador1, indicador2, valor_correlacao) VALUES ('{indicador1}', '{indicador2}', {correlacao_valor})"
        cur.execute(sql)
        conexao.commit()
        exito = True
    except psycopg2.Error as e:
        print(f"Erro ao inserir a correlação no banco de dados: {e}")
        conexao.rollback()
        exito = False
    finally:
        conexao.close()

    return exito